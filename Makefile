compile:
	mvn compile

test:
	mvn test

coverage:
	mvn test jacoco:report

# Geração de testes com EvoSuite
# Certifica-te de que JAVA_HOME aponta para Java 8 antes de executar!
evosuite-generate:
	mvn evosuite:generate \
		-Dcut=Projeto.Utilizador \
		-Dcut=Projeto.Atividade \
		-Dcut=Projeto.PlanoTreino

# Exporta os melhores testes gerados
evosuite-export:
	mvn evosuite:export

mutation:
	mvn test org.pitest:pitest-maven:mutationCoverage

clean:
	mvn clean

clean-hypothesis:
	rm -f src/test/java/Projeto/AtividadePropertyBasedTests.java
	rm -f src/test/java/Projeto/PlanoTreinoPropertyBasedTests.java

clean-evosuite-tests:
	rm -f src/test/java/Projeto/*ESTest*.java

clean-evosuite-all:
	rm -rf .evosuite