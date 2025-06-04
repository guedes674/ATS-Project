import os
from dotenv import load_dotenv
import google.generativeai as genai
from time import sleep # Import sleep for the retry logic

# load environment variables from .env file
load_dotenv()

# load the Gemini API key from an environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    print("Please set it in your .env file or as an environment variable (e.g., export GEMINI_API_KEY='your_key_here').")
    exit(1)

# configure the Gemini API client
genai.configure(api_key=api_key)

# create a Gemini model instance
try:
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error creating Gemini model: {e}")
    print("Please ensure your API key is valid and has access to the model.")
    exit(1)


# define the targets for which we want to generate tests
targets = [
    {
        "class_name": "Projeto.Atividade",
        "methods_focus": "consumoCalorias e getFatorFreqCardiaca. Considere diferentes tipos de atividades (AtivDistancia, AtivRepeticoes, AtivRepsPeso, AtivDistAltimetria) e seus construtores para instanciar nos testes.",
        "file_name": "AtividadeLLMTests.java"
    },
    {
        "class_name": "Projeto.Utilizador",
        "methods_focus": (
            "métodos públicos não abstratos como addAtividade(Atividade), addPlanoTreino(PlanoTreino), "
            "getPlanoTreinoId(int), planosTreinos(LocalDate, LocalDate), "
            "atividadesNumPeriodoQueRespeitamP(LocalDate, LocalDate, Predicate<Atividade>), "
            "e o cálculo de calorias (se houver um método específico para isso ou através de planos/atividades). "
            "Para testar, use subclasses concretas como UtilizadorAmador, UtilizadorPraticanteOcasional ou UtilizadorProfissional."
        ),
        "file_name": "UtilizadorLLMTests.java"
    },
    {
        "class_name": "Projeto.PlanoTreino",
        "methods_focus": (
            "addAtividade(Atividade, int), getAtividades(), getAtividadesNumPeriodo(LocalDate, LocalDate), "
            "atividadesQueRespeitamP(LocalDate, LocalDate, Predicate<Atividade>), caloriasDispendidas(Utilizador), "
            "clone(), compareTo(PlanoTreino), e a lógica da classe interna AtividadeIteracoes (getters, clone, equals). "
            "Certifique-se de testar com diferentes atividades e iterações."
        ),
        "file_name": "PlanoTreinoLLMTests.java"
    }
]

def gemini_generate_text_with_retry(prompt_content, model, retries=3, delay=61):
    """Generates text using Gemini with retry logic for potential API rate limits or temporary issues."""
    for attempt in range(retries):
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=0.5
            )
            response = model.generate_content(
                prompt_content,
                generation_config=generation_config
            )
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                return response
            else:
                print(f"Warning: Received an unexpected response structure on attempt {attempt + 1}: {response}")
                if hasattr(response, 'prompt_feedback'):
                    print(f"Prompt Feedback: {response.prompt_feedback}")
                if response.candidates and response.candidates[0].finish_reason:
                     print(f"Candidate Finish Reason: {response.candidates[0].finish_reason}")
                     if response.candidates[0].safety_ratings:
                        print(f"Candidate Safety Ratings: {response.candidates[0].safety_ratings}")

        except Exception as e:
            print(f"API call failed on attempt {attempt + 1} for prompt targeting {prompt_content[:100]}...: {e}")
            if hasattr(e, 'response') and e.response:
                 print(f"Error details: {e.response}")

        if attempt < retries - 1:
            print(f"Sleeping for {delay} seconds before retrying...")
            sleep(delay)
        else:
            print("Max retries reached. Skipping this target.")
            return None
    return None

# generate tests for each target class
for target in targets:
    print(f"Generating tests for {target['class_name']}...")
    try:
        prompt = (
            "És um programador Java experiente especializado na criação de testes JUnit 5.\n\n"
            f"Gera testes JUnit 5 para a classe `{target['class_name']}`. "
            f"Foca-te nos seguintes aspetos e métodos: {target['methods_focus']}. "
            "O formato deve seguir exatamente este padrão:\n"
            "- Usar JUnit 5 (org.junit.jupiter.api.Test)\n"
            "- Usar static org.junit.jupiter.api.Assertions.*\n"
            "- Usar java.time.LocalDate, LocalDateTime, LocalTime (não Mock)\n"
            "- Nomear métodos com nomes descritivos (ex: testConsumoCalorias, testGetFatorFreqCardiaca)\n"
            "- Usar assertEquals com tolerância 0.01 para valores double\n"
            "- Incluir comentários simples para explicar cada seção do teste\n"
            "- Testar construtores, métodos principais, casos normais e de borda\n"
            "\n"
            "IMPORTANTE - Use os construtores corretos das classes:\n"
            "- UtilizadorAmador(String nome, String morada, String email, int freqCardiaca, int peso, int altura, LocalDate dataNascimento, char genero)\n"
            "- UtilizadorPraticanteOcasional(String nome, String morada, String email, int freqCardiaca, int peso, int altura, LocalDate dataNascimento, char genero)\n"
            "- UtilizadorProfissional(String nome, String morada, String email, int freqCardiaca, int peso, int altura, LocalDate dataNascimento, char genero)\n"
            "- Para atividades, use as subclasses concretas disponíveis no projeto\n"
            "- Use LocalDateTime.of() para datas e horas\n"
            "- Use Duration.ofMinutes() para durações quando necessário\n"
            "\n"
            "Estrutura obrigatória:\n"
            "package Projeto;\n"
            "\n"
            "import org.junit.jupiter.api.Test;\n"
            "import static org.junit.jupiter.api.Assertions.*;\n"
            "import java.time.LocalDate;\n"
            "import java.time.LocalDateTime;\n"
            "import java.time.Duration;\n"
            "// Outras importações necessárias do projeto...\n"
            "\n"
            f"public class {target['class_name'].split('.')[-1]}_LLMTest {{\n"
            "\n"
            "    @Test\n"
            "    void testMetodoExemplo() {\n"
            "        // Object creation\n"
            "        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional(\"Tiago\", \"Rua B\", \"tiago@gmail.com\", 110, 70, 195, LocalDate.of(2002, 12, 4), 'M');\n"
            "        \n"
            "        // Assertions\n"
            "        assertEquals(expected, actual);\n"
            "    }\n"
            "}\n"
            "\n"
            "Gera testes abrangentes cobrindo casos normais, de borda e excecionais quando aplicável. "
            "Inclui testes para construtores, métodos principais como consumoCalorias, getFatorFreqCardiaca, etc. "
            "Usa as subclasses concretas apropriadas (UtilizadorAmador, UtilizadorPraticanteOcasional, UtilizadorProfissional) "
            "e diferentes tipos de atividades conforme apropriado para o projeto. "
            "Inclui comentários simples mas não explicações excessivas. "
            "Certifica-te de que os testes são realistas e funcionais. "
            "NÃO incluas marcação markdown (```java ou ```) na resposta - apenas o código Java puro."
        )

        response_object = gemini_generate_text_with_retry(prompt, gemini_model)

        if response_object and response_object.candidates:
            # extract the generated code from the response
            generated_code = response_object.candidates[0].content.parts[0].text

            # clean the generated code
            if generated_code.startswith("```java"):
                generated_code = generated_code[len("```java"):]
            if generated_code.startswith("```"):
                generated_code = generated_code[len("```"):]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-len("```")]
            generated_code = generated_code.strip()

            # update the target with the class name and file name
            class_name = target['class_name'].split('.')[-1]
            target['file_name'] = f"{class_name}_LLMTest.java"
            
            # define the output directory and file path
            output_directory = "src/test/java/Projeto"
            output_path = os.path.join(output_directory, target['file_name'])
            
            # ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(generated_code)
            print(f"Tests for {target['class_name']} written to {output_path}")
        else:
            print(f"Failed to generate tests for {target['class_name']} after retries or due to unexpected response.")
            if response_object and hasattr(response_object, 'prompt_feedback'):
                 print(f"Prompt Feedback: {response_object.prompt_feedback}")

    except Exception as e:
        print(f"An unexpected error occurred while processing {target['class_name']}: {e}")

print("\nTest generation process complete.")