package Projeto;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class UtilizadorTest {
    @Test
    public void testUtilizadorVazio() {
        // User object creation
        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional();
        utilizador.setNome("João");
        utilizador.setMorada("Rua A");
        utilizador.setEmail("joao@gmail.com");
        utilizador.setFreqCardiaca(80);
        utilizador.setPeso(75);
        utilizador.setAltura(180);
        utilizador.setDataNascimento(LocalDate.of(1990, 1, 1));
        utilizador.setGenero('M');

        // Assertions
        assertEquals("João", utilizador.getNome());
        assertEquals("Rua A", utilizador.getMorada());
        assertEquals("joao@gmail.com", utilizador.getEmail());
        assertEquals(80, utilizador.getFreqCardiaca());
        assertEquals(75, utilizador.getPeso());
        assertEquals(180, utilizador.getAltura());
        assertEquals(LocalDate.of(1990, 1, 1), utilizador.getDataNascimento());
        assertEquals('M', utilizador.getGenero());
    }

    @Test
    public void testUtilizadorParametrizado() {
        //User object creation
        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional("Tiago", "Rua B", "tiago@gmail.com", 100, 70, 195,LocalDate.of(2002, 12, 4) , 'M');

        // Assertions
        assertEquals("Tiago", utilizador.getNome());
        assertEquals("Rua B", utilizador.getMorada());
        assertEquals("tiago@gmail.com", utilizador.getEmail());
        assertEquals(100, utilizador.getFreqCardiaca());
        assertEquals(70, utilizador.getPeso());
        assertEquals(195, utilizador.getAltura());
        assertEquals(LocalDate.of(2002, 12, 4), utilizador.getDataNascimento());
        assertEquals('M', utilizador.getGenero());
    }

    @Test
    public void testUtilizadorIdade() {
        // User object creation
        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional("Tiago", "Rua B", "tiago@gmail.com", 100, 70, 195,LocalDate.of(2002, 12, 4) , 'M');

        // Assertions
        assertEquals(23, utilizador.getIdade());
    }

    @Test
    public void testUtilizadorAddAtividade() {
        // User and activity object creation
        UtilizadorPraticanteOcasional utilizador = new UtilizadorPraticanteOcasional("Tiago", "Rua B", "tiago@gmail.com", 100, 70, 195,LocalDate.of(2002, 12, 4) , 'M');
        AtivDistancia atividade = new Ciclismo(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 30), 120, 10.0);
        AtivRepeticoes atividade2 = new Abdominais(LocalDateTime.of(2023, 10, 1, 10, 0), LocalTime.of(0, 8), 120, 50);

        // Add activity to user
        utilizador.addAtividade(atividade);
        utilizador.addAtividade(atividade2);

        // Assertions
        assertEquals(2, utilizador.getAtividadesIsoladas().size());
        assertEquals(atividade, utilizador.getAtividadesIsoladas().get(0));
        assertEquals(atividade2, utilizador.getAtividadesIsoladas().get(1));
    }
}