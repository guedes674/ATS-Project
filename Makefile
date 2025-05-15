# compile:
# 	mvn compile

# test:
# 	mvn test

# coverage:
# 	mvn test jacoco:report

# mutation:
# 	mvn test org.pitest:pitest-maven:mutationCoverage

# # evosuite (not working yet)
# evosuite-setup:
# 	fish -c "set -x JAVA_HOME /usr/lib/jvm/java-8-openjdk; set -x MAVEN_OPTS '-Djava.home=$JAVA_HOME'"

# # evosuite (not working yet)
# evosuite-generate: evosuite-setup
# 	mvn evosuite:generate -Dcut=Projeto.Utilizador -Dcut=Projeto.Atividade -Dcut=Projeto.PlanoTreino

# # evosuite (not working yet)
# evosuite-export:
# 	mvn evosuite:export

# clean:
# 	mvn clean

# # evosuite (not working yet)
# clean-evosuite-tests:
# 	rm -f src/test/java/Projeto/*ESTest*.java

# # evosuite (not working yet)
# clean-evosuite-all:
# 	rm -rf .evosuite


# ----------------------------------------------------------------------------------------
compile:
	mvn compile

test:
	mvn test

coverage:
	mvn test jacoco:report

mutation:
	mvn test org.pitest:pitest-maven:mutationCoverage

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

clean:
	mvn clean

clean-evosuite-tests:
	rm -f src/test/java/Projeto/*ESTest*.java

clean-evosuite-all:
	rm -rf .evosuite
