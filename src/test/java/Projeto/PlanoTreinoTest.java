package Projeto;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class PlanoTreinoTest {
    @Test
    public void testPlanoTreinoVazio(){
        PlanoTreino pt = new PlanoTreino();
        AtivDistancia ciclismo = new Ciclismo(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);
        AtivDistancia corrida = new Corrida(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);
        pt.addAtividade(ciclismo, 5);
        pt.addAtividade(corrida, 5);
        pt.setDataRealizacao(LocalDate.of(2023, 10, 1));
        assertEquals(pt.getCodPlano(), 0);
        assertEquals(pt.getAtividades().size(), 2);
        assertEquals(pt.getDataRealizacao(), LocalDate.of(2023, 10, 1));
    }

    @Test
    public void testPlanoTreinoParametrizado(){
        PlanoTreino pt = new PlanoTreino(LocalDate.of(2023, 10, 1));
        AtivDistancia ciclismo = new Ciclismo(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);
        AtivDistancia corrida = new Corrida(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);
        pt.addAtividade(ciclismo, 5);
        pt.addAtividade(corrida, 5);
        assertEquals(pt.getCodPlano(), 1);
        assertEquals(pt.getAtividades().size(), 2);
        assertEquals(pt.getDataRealizacao(), LocalDate.of(2023, 10, 1));
    }
}