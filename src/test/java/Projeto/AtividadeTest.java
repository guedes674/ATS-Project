package Projeto;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class AtividadeTest {
    @Test
    public void testAtividadeVazia() {
        // Activity object creation
        AtivDistancia atividade = new Ciclismo();
        atividade.setDataRealizacao(LocalDateTime.of(2023, 10, 1, 10, 0));
        atividade.setTempo(LocalTime.of(0, 30));
        atividade.setFreqCardiaca(120);
        atividade.setDistancia(15.0);

        // Assertions
        assertEquals(LocalDateTime.of(2023, 10, 1, 10, 0), atividade.getDataRealizacao());
        assertEquals(LocalTime.of(0, 30), atividade.getTempo());
        assertEquals(120, atividade.getFreqCardiaca());
        assertEquals(15.0, atividade.getDistancia());
    }

    @Test
    public void testAtividadeParametrizada() {
        // Activity object creation
        AtivDistancia atividade = new Ciclismo(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);

        // Assertions
        assertEquals(LocalDateTime.of(2023, 10, 1, 10, 0), atividade.getDataRealizacao());
        assertEquals(LocalTime.of(0, 30), atividade.getTempo());
        assertEquals(120, atividade.getFreqCardiaca());
        assertEquals(10.0, atividade.getDistancia());
    }

    @Test
    public void testConsumoCalorias() {
        // Activity and User object creation
        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional("Tiago", "Rua B", "tiago@gmail.com",110, 70, 195,LocalDate.of(2002, 12, 4) , 'M');
        AtivRepeticoes atividade = new Abdominais(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 8), 120, 50);

        // Assertions
        assertEquals(8.5, atividade.consumoCalorias(utilizador), 0.01);
    }

    @Test
    public void testGetVelocidade() {
        // Activity and User object creation
        AtivDistancia atividade = new Corrida(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 10), 120, 1200.0);

        // Assertions
        assertEquals(2.0, atividade.getVelocidade());
    }
}