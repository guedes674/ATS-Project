import datetime
import os
import re
from datetime import date
time_re = re.compile(r"LocalTime\.of\((\d+),\s*(\d+),\s*(\d+)\)")

import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings

# Shared primitive strategies
st_string_short = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(whitelist_categories=("L", "Nd")),
)
st_string_long = st.text(
    min_size=5,
    max_size=200,
    alphabet=st.characters(whitelist_categories=("L", "Nd", "P", "Z")),
)
st_freq_cardiaca = st.integers(40, 220)
st_peso = st.floats(10.0, 300.0, allow_nan=False, allow_infinity=False, width=64)
st_altura = st.integers(50, 250)
st_genero = st.just("M") | st.just("F")
st_distancia = st.floats(0.0, 100_000.0, width=64)
st_altimetria = st.floats(0.0, 5_000.0, width=64)
st_repeticoes = st.integers(0, 5_000)
st_tempo_seconds = st.integers(1, 86_400)

# java.time helpers
@st.composite
def st_local_date_time(draw):
    dt = draw(
        st.datetimes(
            min_value=datetime.datetime(2000, 1, 1),
            max_value=datetime.datetime(2030, 12, 31),
        )
    )
    return (
        f"LocalDateTime.of({dt.year}, {dt.month}, {dt.day}, "
        f"{dt.hour}, {dt.minute}, {dt.second})"
    )


@st.composite
def st_local_time(draw):
    t = draw(st.times(min_value=datetime.time(0, 0, 1)))
    return f"LocalTime.of({t.hour}, {t.minute}, {t.second})"


@st.composite
def st_local_date(draw):
    d = draw(st.dates(min_value=date(1900, 1, 1), max_value=date.today()))
    return f"LocalDate.of({d.year}, {d.month}, {d.day})"


# Parameter dictionaries for each Atividade kind
@st.composite
def st_base_atividade_params(draw):
    return {
        "realizacao_str": draw(st_local_date_time()),
        "tempo_str": draw(st_local_time()),
        "tempo_seconds": draw(st_tempo_seconds),
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


# Java-construction snippets
@st.composite
def st_ciclismo_instance(draw):
    p = draw(st_ciclismo_params())
    return {
        **p,
        "java_code": (
            "new Ciclismo("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['distancia']}d)"
        ),
    }


@st.composite
def st_btt_instance(draw):
    p = draw(st_btt_params())
    return {
        **p,
        "java_code": (
            "new Btt("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['distancia']}d, {p['altimetria']}d)"
        ),
    }


@st.composite
def st_flexoes_instance(draw):
    p = draw(st_flexoes_params())
    return {
        **p,
        "java_code": (
            "new Flexoes("
            f"{p['realizacao_str']}, {p['tempo_str']}, "
            f"{p['freqCardiaca']}, {p['repeticoes']})"
        ),
    }


st_any_concrete_atividade_instance = st.one_of(
    st_ciclismo_instance(), st_btt_instance(), st_flexoes_instance()
)

# Email & Utilizador params
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


st_utilizador_params_for_activity_test = st.fixed_dictionaries(
    {
        "nome": st_string_short,
        "morada": st_string_short,
        "email": st_email(),
        "freqCardiaca": st_freq_cardiaca,
        "peso": st_peso,
        "altura": st_altura,
        "dataNascimento": st_local_date(),
        "genero": st_genero,
    }
)

# JUnit test templates
CICLISMO_CONSTRUCTOR_TEST_TEMPLATE = """
    @Test
    public void testCiclismoConstructor_{test_id}() {{
        LocalDateTime dataRealizacao = {realizacao_str};
        LocalTime     tempo          = {tempo_str};
        int           freqCardiaca   = {freqCardiaca};
        double        distancia      = {distancia}d;

        Ciclismo atividade = new Ciclismo(dataRealizacao, tempo,
                                          freqCardiaca, distancia);

        assertNotNull(atividade.getCodAtividade());
        assertEquals(dataRealizacao, atividade.getDataRealizacao());
        assertEquals(tempo,          atividade.getTempo());
        assertEquals(freqCardiaca,   atividade.getFreqCardiaca());
        assertEquals(distancia,      atividade.getDistancia(), 0.001);
    }}
""".strip()

BTT_CONSTRUCTOR_TEST_TEMPLATE = """
    @Test
    public void testBttConstructor_{test_id}() {{
        LocalDateTime dataRealizacao = {realizacao_str};
        LocalTime     tempo          = {tempo_str};
        int           freqCardiaca   = {freqCardiaca};
        double        distancia      = {distancia}d;
        double        altimetria     = {altimetria}d;

        Btt atividade = new Btt(dataRealizacao, tempo, freqCardiaca,
                                distancia, altimetria);

        assertNotNull(atividade.getCodAtividade());
        assertEquals(dataRealizacao, atividade.getDataRealizacao());
        assertEquals(tempo,          atividade.getTempo());
        assertEquals(freqCardiaca,   atividade.getFreqCardiaca());
        assertEquals(distancia,      atividade.getDistancia(), 0.001);
        assertEquals(altimetria,     atividade.getAltimetria(), 0.001);
    }}
""".strip()

FLEXOES_CONSTRUCTOR_TEST_TEMPLATE = """
    @Test
    public void testFlexoesConstructor_{test_id}() {{
        LocalDateTime dataRealizacao = {realizacao_str};
        LocalTime     tempo          = {tempo_str};
        int           freqCardiaca   = {freqCardiaca};
        int           repeticoes     = {repeticoes};

        Flexoes atividade = new Flexoes(dataRealizacao, tempo,
                                        freqCardiaca, repeticoes);

        assertNotNull(atividade.getCodAtividade());
        assertEquals(dataRealizacao, atividade.getDataRealizacao());
        assertEquals(tempo,          atividade.getTempo());
        assertEquals(freqCardiaca,   atividade.getFreqCardiaca());
        assertEquals(repeticoes,     atividade.getRepeticoes());
    }}
""".strip()

ATIVIDADE_FATOR_FREQ_CARD_TEST_TEMPLATE = """
    @Test
    public void testGetFatorFreqCardiaca_{test_id}() {{
        int userFreqCardiaca = {user_freq_cardiaca};
        Utilizador user = new UtilizadorProfissional(
            "Dummy", "Addr", "x@y.com",
            userFreqCardiaca, 70, 170, LocalDate.of(1990, 1, 1), 'M');

        {atividade_creation_code};

        double razao = (double) user.getFreqCardiaca()
                       / (atividade.getFreqCardiaca() == 0 ? 1
                                                            : atividade.getFreqCardiaca());
        double expected = (razao - 2) * 0.4;

        assertEquals(expected,
                     atividade.getFatorFreqCardiaca(user), 0.001);
    }}
""".strip()

BTT_CONSUMO_CALORIAS_TEST_TEMPLATE = """
    @Test
    public void testBttConsumoCalorias_{test_id}() {{
        double userPeso         = {user_peso}d;
        int    userAltura       = {user_altura};
        LocalDate nascimento    = {user_data_nascimento};
        char   genero           = '{user_genero}';
        int    userFreqCardiaca = {user_freq_cardiaca};

        UtilizadorProfissional user = new UtilizadorProfissional(
            "Teste", "Addr", "e@mail.com",
            userFreqCardiaca, (int) userPeso, userAltura,
            nascimento, genero);
        user.setPeso(userPeso); user.setAltura(userAltura);

        LocalDateTime dataRealizacao = {realizacao_str};
        LocalTime     tempo          = {tempo_str};
        int tempoSeconds             = {tempo_seconds};
        int freqCardiaca             = {atividade_freq_cardiaca};
        double distancia             = {distancia}d;
        double altimetria            = {altimetria}d;

        Btt btt = new Btt(dataRealizacao, tempo, freqCardiaca,
                          distancia, altimetria);

        double fMult = 1.5;
        double fVel  = (distancia / tempoSeconds - 10.5) * 0.11;
        double fFreq = ((double) userFreqCardiaca / freqCardiaca - 2) * 0.4;
        double fAlt  = altimetria * 0.0005;

        int age   = LocalDate.now().getYear() - nascimento.getYear();
        int sVal  = genero == 'M' ? 5 : -161;
        double bmr = 10*userPeso + 6.25*userAltura + 5*age + sVal;

        double fHard = 1.05;
        if (altimetria > 1000) fHard += 0.10;
        if (altimetria > 2000) fHard += 0.10;

        // MET is 10 in BTT
        double expected = 10 * (fMult + fVel + fFreq + fAlt)
                          * bmr / (24.0*60*60)
                          * fHard * tempoSeconds;
        //expected = Math.max(0.0, expected);

        assertEquals(expected, btt.consumoCalorias(user), 0.01);
    }}
""".strip()

# Scenario builders
@st.composite
def ciclismo_constructor_scenario(draw):
    p = draw(st_ciclismo_params())
    return CICLISMO_CONSTRUCTOR_TEST_TEMPLATE.format(
        test_id=abs(hash(frozenset(p.items()))) % 1_000_000,
        **p,
    )


@st.composite
def btt_constructor_scenario(draw):
    p = draw(st_btt_params())
    return BTT_CONSTRUCTOR_TEST_TEMPLATE.format(
        test_id=abs(hash(frozenset(p.items()))) % 1_000_000,
        **p,
    )


@st.composite
def flexoes_constructor_scenario(draw):
    p = draw(st_flexoes_params())
    return FLEXOES_CONSTRUCTOR_TEST_TEMPLATE.format(
        test_id=abs(hash(frozenset(p.items()))) % 1_000_000,
        **p,
    )


@st.composite
def atividade_fator_freq_card_scenario(draw):
    user = draw(st_utilizador_params_for_activity_test)
    atv = draw(st_any_concrete_atividade_instance)
    return ATIVIDADE_FATOR_FREQ_CARD_TEST_TEMPLATE.format(
        test_id=abs(hash((user["freqCardiaca"], frozenset(atv.items())))) % 1_000_000,
        user_freq_cardiaca=user["freqCardiaca"],
        atividade_creation_code=f"Atividade atividade = {atv['java_code']}",
    )


@st.composite
def btt_consumo_calorias_scenario(draw):
    user = draw(st_utilizador_params_for_activity_test)
    btt = draw(st_btt_params())
    btt["tempo_seconds"] = max(1, btt["tempo_seconds"])
    return BTT_CONSUMO_CALORIAS_TEST_TEMPLATE.format(
        test_id=abs(hash((frozenset(user.items()), frozenset(btt.items()))))
        % 1_000_000,
        user_peso=user["peso"],
        user_altura=user["altura"],
        user_data_nascimento=user["dataNascimento"],
        user_genero=user["genero"],
        user_freq_cardiaca=user["freqCardiaca"],
        atividade_freq_cardiaca=btt["freqCardiaca"],
        **btt,
    )


# Consolidated strategy
st_all_atividade_scenarios = st.one_of(
    ciclismo_constructor_scenario(),
    btt_constructor_scenario(),
    flexoes_constructor_scenario(),
    atividade_fator_freq_card_scenario(),
    btt_consumo_calorias_scenario(),
)

def make_unique(methods):
    seen, uniq = set(), []
    sig_re = re.compile(r"void\s+([^(]+)\(")
    for m in methods:
        sig = sig_re.search(m).group(1)
        if sig not in seen:
            seen.add(sig)
            uniq.append(m)
    return uniq


# Java-class creation
def generate_test_class(class_name, methods):
    header = """
package Projeto;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

import Projeto.Utilizador;
import Projeto.UtilizadorProfissional;
import Projeto.Btt;
import Projeto.Ciclismo;
import Projeto.Flexoes;

""".rstrip()

    return f"{header}\n\npublic class {class_name} {{\n" + "\n".join(methods) + "\n}\n"


# Collect methods
ALL_METHODS = []


@settings(max_examples=20, suppress_health_check=[HealthCheck.filter_too_much])
@given(m=st_all_atividade_scenarios)
def collect(m):
    ALL_METHODS.append(m)


if __name__ == "__main__":
    CLASS_NAME = "AtividadePropertyBasedTests"
    OUTPUT_FILE = "../java/Projeto/AtividadePropertyBasedTests.java"

    collect()

    if not ALL_METHODS:
        print("No tests generated.")
        raise SystemExit

    java_code = generate_test_class(CLASS_NAME, make_unique(ALL_METHODS))
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(java_code)

    print("Generated JUnit tests -> ", OUTPUT_FILE)
