import datetime
import os
import re
from datetime import date

import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings

# creating the default strategies
st_string_short = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(whitelist_categories=("L", "Nd")),
)
st_freq_cardiaca = st.integers(40, 220)
st_peso = st.floats(10.0, 300.0, allow_nan=False, allow_infinity=False, width=64)
st_altura = st.integers(50, 250)
st_distancia = st.floats(0.0, 100_000.0, width=64)
st_altimetria = st.floats(0.0, 5_000.0, width=64)
st_repeticoes = st.integers(0, 5_000)
st_tempo_seconds = st.integers(1, 3600 * 4) # 4 hours to limit the time duration

# --- java.time helpers ---
@st.composite
def st_local_date_time(draw):
    dt = draw(
        st.datetimes(
            min_value=datetime.datetime(2020, 1, 1),
            max_value=datetime.datetime(2025, 12, 31),
        )
    )
    return (
        f"LocalDateTime.of({dt.year}, {dt.month}, {dt.day}, "
        f"{dt.hour}, {dt.minute}, {dt.second})"
    )

@st.composite
def st_local_time(draw):
    t = draw(st.times(min_value=datetime.time(0, 0, 30), max_value=datetime.time(0, 8, 0))) # make sure time is greater than 30 seconds and less than 8 hours
    return f"LocalTime.of({t.hour}, {t.minute}, {t.second})"

@st.composite
def st_local_date(draw):
    d = draw(st.dates(min_value=date(2020, 1, 1), max_value=date(2025, 12, 31)))
    return f"LocalDate.of({d.year}, {d.month}, {d.day})"

# --- Atividade strategies ---
@st.composite
def st_base_atividade_params(draw):
    return {
        "realizacao_str": draw(st_local_date_time()),
        "tempo_str": draw(st_local_time()),
        "freqCardiaca": draw(st_freq_cardiaca),
    }

@st.composite
def st_ciclismo_params(draw):
    p = draw(st_base_atividade_params())
    p["distancia"] = draw(st_distancia)
    return p

@st.composite
def st_btt_params(draw):
    p = draw(st_base_atividade_params())
    p["distancia"] = draw(st_distancia)
    p["altimetria"] = draw(st_altimetria)
    return p

@st.composite
def st_flexoes_params(draw):
    p = draw(st_base_atividade_params())
    p["repeticoes"] = draw(st_repeticoes)
    return p

@st.composite
def st_ciclismo_instance_details(draw):
    p = draw(st_ciclismo_params())
    return {
        "params": p,
        "java_code": (
            "new Ciclismo("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['distancia']}d)"
        ),
        "type": "Ciclismo",
    }

@st.composite
def st_btt_instance_details(draw):
    p = draw(st_btt_params())
    return {
        "params": p,
        "java_code": (
            "new Btt("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['distancia']}d, {p['altimetria']}d)"
        ),
        "type": "Btt",
    }

@st.composite
def st_flexoes_instance_details(draw):
    p = draw(st_flexoes_params())
    return {
        "params": p,
        "java_code": (
            "new Flexoes("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['repeticoes']})"
        ),
        "type": "Flexoes",
    }

st_any_concrete_atividade_details = st.one_of(
    st_ciclismo_instance_details(), st_btt_instance_details(), st_flexoes_instance_details()
)

# --- Utilizador strategies ---
@st.composite
def st_email(draw):
    part = lambda: draw(
        st.text(
            min_size=1,
            max_size=10,
            alphabet=st.characters(whitelist_categories=("L", "Nd")),
        )
    ).lower()
    return f"{part()}@{part()}.{part()}"

@st.composite
def st_utilizador_details(draw, use_default_constructor=False):
    user_class_name = draw(st.sampled_from(["UtilizadorAmador", "UtilizadorProfissional", "UtilizadorPraticanteOcasional"]))
    
    if use_default_constructor:
        java_code = f"new {user_class_name}()"
        return {"java_code": java_code, "class_name": user_class_name}

    nome = draw(st_string_short)
    morada = draw(st_string_short)
    email_str = draw(st_email())
    freq_card_media = draw(st_freq_cardiaca)
    user_peso = draw(st_peso)
    user_altura = draw(st_altura)
    data_nasc_str = draw(st_local_date())
    genero = draw(st.sampled_from(['M', 'F']))

    peso_param_str = f"{user_peso}d" if "Amador" in user_class_name or "Ocasional" in user_class_name else f"(int){user_peso}"


    java_code = (
        f"new {user_class_name}(\"{nome}\", \"{morada}\", \"{email_str}\", "
        f"{freq_card_media}, {peso_param_str}, {user_altura}, "
        f"{data_nasc_str}, '{genero}')"
    )
    
    return {
        "java_code": java_code,
        "class_name": user_class_name,
        "nome": nome, "morada": morada, "email": email_str,
        "freq_card_media": freq_card_media, "peso": user_peso, "altura": user_altura,
        "data_nascimento_str": data_nasc_str, "genero": genero,
    }

# --- PlanoTreino specific strategies ---
st_iteracoes = st.integers(5, 30) # reasonable limit for iterations

@st.composite
def st_plano_treino_construction_details(draw):
    use_date_constructor = draw(st.booleans())
    data_realizacao_str = None
    constructor_call = "new PlanoTreino()"
    if use_date_constructor:
        data_realizacao_str = draw(st_local_date())
        constructor_call = f"new PlanoTreino({data_realizacao_str})"
    
    return {
        "constructor_call": constructor_call,
        "data_realizacao_str": data_realizacao_str
    }

# --- JUnit test templates for PlanoTreino ---
PLANO_TREINO_DATE_CONSTRUCTOR_TEST_TEMPLATE = """
    @Test
    public void testPlanoTreinoDateConstructor_{test_id}() {{
        LocalDate data = {data_realizacao_str};
        PlanoTreino plano = new PlanoTreino(data);
        assertNotNull(plano);
        assertEquals(data, plano.getDataRealizacao());
        assertTrue(plano.getAtividades().isEmpty());
        assertTrue(plano.getCodPlano() >= 0);
    }}
""".strip()

PLANO_TREINO_ADD_GET_ATIVIDADES_TEST_TEMPLATE = """
    @Test
    public void testPlanoTreinoAddAndGetAtividades_{test_id}() {{
        PlanoTreino plano = {plano_constructor_call};
        
        Atividade atividade1 = {atividade1_java_code};
        int iteracoes1 = {iteracoes1};
        plano.addAtividade(atividade1, iteracoes1);

        assertEquals(1, plano.getAtividades().size());
        PlanoTreino.AtividadeIteracoes ai1 = plano.getAtividades().get(0);
        assertEquals(iteracoes1, ai1.getIteracoes());
        assertEquals(atividade1.getCodAtividade(), ai1.getAtividade().getCodAtividade()); 

        Atividade atividade2 = {atividade2_java_code};
        int iteracoes2 = {iteracoes2};
        plano.addAtividade(atividade2, iteracoes2);
        
        assertEquals(2, plano.getAtividades().size());
    }}
""".strip()

PLANO_TREINO_CLONE_TEST_TEMPLATE = """
    @Test
    public void testPlanoTreinoClone_{test_id}() {{
        PlanoTreino originalPlano = {plano_constructor_call};
        LocalDate originalDate = originalPlano.getDataRealizacao();

        Atividade atividade = {atividade_java_code};
        int iteracoes = {iteracoes};
        originalPlano.addAtividade(atividade, iteracoes);

        PlanoTreino clonedPlano = (PlanoTreino) originalPlano.clone();

        assertNotNull(clonedPlano);
        assertNotSame(originalPlano, clonedPlano);
        assertEquals(originalPlano.getCodPlano(), clonedPlano.getCodPlano());
        assertEquals(originalDate, clonedPlano.getDataRealizacao());
        
        assertEquals(originalPlano.getAtividades().size(), clonedPlano.getAtividades().size());
        if (!originalPlano.getAtividades().isEmpty()) {{
            PlanoTreino.AtividadeIteracoes originalAI = originalPlano.getAtividades().get(0);
            PlanoTreino.AtividadeIteracoes clonedAI = clonedPlano.getAtividades().get(0);
            assertNotSame(originalAI, clonedAI);
            assertEquals(originalAI.getIteracoes(), clonedAI.getIteracoes());
            assertNotSame(originalAI.getAtividade(), clonedAI.getAtividade());
            assertEquals(originalAI.getAtividade().getCodAtividade(), clonedAI.getAtividade().getCodAtividade());
        }}
    }}
""".strip()

PLANO_TREINO_COMPARE_TO_TEST_TEMPLATE = """
    @Test
    public void testPlanoTreinoCompareTo_{test_id}() {{
        PlanoTreino plano1 = {plano1_constructor_call};
        Atividade atividade1 = {atividade1_java_code};
        int iteracoes1 = {iteracoes1};
        plano1.addAtividade(atividade1, iteracoes1);

        PlanoTreino plano2 = {plano2_constructor_call};
        Atividade atividade2 = {atividade2_java_code};
        int iteracoes2 = {iteracoes2};
        plano2.addAtividade(atividade2, iteracoes2);

        LocalDate p1Date = plano1.getDataRealizacao();
        LocalDate p2Date = plano2.getDataRealizacao();
        int p1Cod = plano1.getCodPlano();
        int p2Cod = plano2.getCodPlano();

        int expectedComparisonSign;
        if (p1Date == null) {{
            if (p2Date == null) {{
                expectedComparisonSign = Integer.signum(p1Cod - p2Cod);
            }} else {{
                expectedComparisonSign = -1;
            }}
        }} else {{
            if (p2Date == null) {{
                expectedComparisonSign = 1;
            }} else {{
                int dateCompare = p1Date.compareTo(p2Date);
                if (dateCompare != 0) {{
                    expectedComparisonSign = Integer.signum(dateCompare);
                }} else {{
                    expectedComparisonSign = Integer.signum(p1Cod - p2Cod);
                }}
            }}
        }}

        int actualComparisonResult = plano1.compareTo(plano2);
        assertEquals(expectedComparisonSign, Integer.signum(actualComparisonResult),
            String.format("plano1.compareTo(plano2) sign mismatch.\\nP1(Date:%s, Code:%d), P2(Date:%s, Code:%d).\\nExpectedSign:%d, ActualVal:%d (ActualSign:%d)",
                          p1Date, p1Cod, p2Date, p2Cod,
                          expectedComparisonSign, actualComparisonResult, Integer.signum(actualComparisonResult)));

        assertEquals(0, plano1.compareTo(plano1), "Reflexivity check: plano1.compareTo(plano1) should be 0.");

        int reverseActualComparisonResult = plano2.compareTo(plano1);
        assertEquals(expectedComparisonSign, -Integer.signum(reverseActualComparisonResult),
            String.format("Antisymmetry check: sgn(p1.compareTo(p2)) != -sgn(p2.compareTo(p1)).\\nP1(Date:%s, Code:%d), P2(Date:%s, Code:%d).\\nExpectedSign P1vsP2:%d, ActualSign P2vsP1:%d",
                          p1Date, p1Cod, p2Date, p2Cod,
                          expectedComparisonSign, Integer.signum(reverseActualComparisonResult)));
    }}
""".strip()

# --- Scenario builders ---
@st.composite
def plano_treino_date_constructor_scenario(draw):
    data_str = draw(st_local_date())
    return PLANO_TREINO_DATE_CONSTRUCTOR_TEST_TEMPLATE.format(
        test_id=abs(hash(data_str)) % 1_000_000,
        data_realizacao_str=data_str
    )

@st.composite
def plano_treino_add_get_atividades_scenario(draw):
    construction_details = draw(st_plano_treino_construction_details())
    ativ1_details = draw(st_any_concrete_atividade_details)
    iters1 = draw(st_iteracoes)
    ativ2_details = draw(st_any_concrete_atividade_details)
    iters2 = draw(st_iteracoes)
    
    return PLANO_TREINO_ADD_GET_ATIVIDADES_TEST_TEMPLATE.format(
        test_id=abs(hash((construction_details["constructor_call"], ativ1_details["java_code"], iters1, ativ2_details["java_code"], iters2))) % 1_000_000,
        plano_constructor_call=construction_details["constructor_call"],
        atividade1_java_code=ativ1_details["java_code"],
        iteracoes1=iters1,
        atividade2_java_code=ativ2_details["java_code"],
        iteracoes2=iters2,
    )

@st.composite
def plano_treino_clone_scenario(draw):
    construction_details = draw(st_plano_treino_construction_details())
    ativ_details = draw(st_any_concrete_atividade_details)
    iters = draw(st_iteracoes)
    return PLANO_TREINO_CLONE_TEST_TEMPLATE.format(
        test_id=abs(hash((construction_details["constructor_call"], ativ_details["java_code"], iters))) % 1_000_000,
        plano_constructor_call=construction_details["constructor_call"],
        atividade_java_code=ativ_details["java_code"],
        iteracoes=iters
    )

@st.composite
def plano_treino_compare_to_scenario(draw):
    construction1_details = draw(st_plano_treino_construction_details())
    ativ1_details = draw(st_any_concrete_atividade_details)
    iters1 = draw(st_iteracoes)

    construction2_details = draw(st_plano_treino_construction_details())
    ativ2_details = draw(st_any_concrete_atividade_details)
    iters2 = draw(st_iteracoes)
    
    test_id_hash_tuple = (
        construction1_details["constructor_call"], ativ1_details["java_code"], iters1,
        construction2_details["constructor_call"], ativ2_details["java_code"], iters2,
        "compare_to_populated"
    )

    return PLANO_TREINO_COMPARE_TO_TEST_TEMPLATE.format(
        test_id=abs(hash(test_id_hash_tuple)) % 1_000_000,
        plano1_constructor_call=construction1_details["constructor_call"],
        atividade1_java_code=ativ1_details["java_code"],
        iteracoes1=iters1,
        plano2_constructor_call=construction2_details["constructor_call"],
        atividade2_java_code=ativ2_details["java_code"],
        iteracoes2=iters2
    )

@st.composite
def plano_treino_compare_to_same_activity_scenario(draw):
    construction1_details = draw(st_plano_treino_construction_details())
    construction2_details = draw(st_plano_treino_construction_details())

    common_ativ_details = draw(st_any_concrete_atividade_details)
    common_iters = draw(st_iteracoes)

    test_id_hash_tuple = (
        construction1_details["constructor_call"],
        construction2_details["constructor_call"],
        common_ativ_details["java_code"], common_iters,
        "compare_to_same_activity"
    )

    return PLANO_TREINO_COMPARE_TO_TEST_TEMPLATE.format(
        test_id=abs(hash(test_id_hash_tuple)) % 1_000_000,
        plano1_constructor_call=construction1_details["constructor_call"],
        atividade1_java_code=common_ativ_details["java_code"],
        iteracoes1=common_iters,
        plano2_constructor_call=construction2_details["constructor_call"],
        atividade2_java_code=common_ativ_details["java_code"],
        iteracoes2=common_iters
    )

# --- Consolidated strategy ---
st_all_plano_treino_scenarios = st.one_of(
    plano_treino_date_constructor_scenario(),
    plano_treino_add_get_atividades_scenario(),
    plano_treino_clone_scenario(),
    plano_treino_compare_to_scenario(),
    plano_treino_compare_to_same_activity_scenario()
)

# --- Java class generation ---
def make_unique(methods):
    seen, uniq = set(), []
    sig_re = re.compile(r"void\s+([^(]+)\(")
    for m_code in methods:
        match = sig_re.search(m_code)
        if match:
            sig = match.group(1)
            if sig not in seen:
                seen.add(sig)
                uniq.append(m_code)
        else:
            uniq.append(m_code)
    return uniq

def generate_test_class(class_name, methods_code):
    header = """
package Projeto;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

import Projeto.Atividade;
import Projeto.Btt;
import Projeto.Ciclismo;
import Projeto.Flexoes;

import Projeto.Utilizador;
import Projeto.UtilizadorAmador;
import Projeto.UtilizadorProfissional;
import Projeto.UtilizadorPraticanteOcasional;

import Projeto.PlanoTreino;

""".rstrip()
    indented_methods = ["    " + method.replace("\n", "\n    ") for method in methods_code]
    
    return f"{header}\n\npublic class {class_name} {{\n" + "\n\n".join(indented_methods) + "\n}\n"

# --- Main execution ---
ALL_METHODS_CODE = []

@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.data_too_large, HealthCheck.too_slow]) # Reduced examples for speed
@given(m_code=st_all_plano_treino_scenarios)
def collect_plano_treino_methods(m_code):
    ALL_METHODS_CODE.append(m_code)

if __name__ == "__main__":
    CLASS_NAME = "PlanoTreinoPropertyBasedTests"
    OUTPUT_FILE = "../java/Projeto/PlanoTreinoPropertyBasedTests.java" 
    OUTPUT_FILE = os.path.join(
        os.path.dirname(__file__),
        "..",
        "java",
        "Projeto",
        f"{CLASS_NAME}.java"
    )
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    OUTPUT_FILE = os.path.join(project_root, "src", "test", "java", "Projeto", f"{CLASS_NAME}.java")

    collect_plano_treino_methods()

    if not ALL_METHODS_CODE:
        print("No tests generated for PlanoTreino.")
    else:
        unique_methods = make_unique(ALL_METHODS_CODE)
        java_code_output = generate_test_class(CLASS_NAME, unique_methods)
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(java_code_output)
        print(f"Generated JUnit tests for PlanoTreino -> {OUTPUT_FILE}")