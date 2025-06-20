/*
 * This file was automatically generated by EvoSuite
 * Wed Jun 04 15:25:49 GMT 2025
 */

package Projeto;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import Projeto.Abdominais;
import Projeto.Atividade;
import Projeto.BenchPress;
import Projeto.BicepCurls;
import Projeto.Btt;
import Projeto.Ciclismo;
import Projeto.Corrida;
import Projeto.Flexoes;
import Projeto.LegPress;
import Projeto.Trail;
import Projeto.Utilizador;
import Projeto.UtilizadorAmador;
import Projeto.UtilizadorPraticanteOcasional;
import Projeto.UtilizadorProfissional;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;
import java.time.Period;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.chrono.IsoChronology;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.evosuite.runtime.mock.java.time.MockInstant;
import org.evosuite.runtime.mock.java.time.MockLocalDate;
import org.evosuite.runtime.mock.java.time.MockLocalDateTime;
import org.evosuite.runtime.mock.java.time.MockLocalTime;
import org.evosuite.runtime.mock.java.time.chrono.MockIsoChronology;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Atividade_ESTest extends Atividade_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Flexoes flexoes0 = new Flexoes();
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador();
      Atividade atividade0 = flexoes0.geraAtividade(utilizadorAmador0, 0.0);
      int int0 = atividade0.compareTo((Atividade) flexoes0);
      assertTrue(atividade0.equals((Object)flexoes0));
      assertEquals(1, flexoes0.getCodAtividade());
      assertEquals(1, int0);
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Corrida corrida0 = new Corrida();
      Corrida corrida1 = new Corrida(corrida0);
      int int0 = corrida1.compareTo((Atividade) corrida0);
      assertEquals(0, int0);
      assertEquals(1, corrida0.getCodAtividade());
      assertTrue(corrida0.equals((Object)corrida1));
      assertEquals(0, corrida1.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      BenchPress benchPress1 = new BenchPress();
      benchPress1.setFreqCardiaca(680);
      boolean boolean0 = benchPress1.equals(benchPress0);
      assertEquals(680, benchPress1.getFreqCardiaca());
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      LegPress legPress0 = new LegPress();
      String string0 = legPress0.toString();
      assertEquals("Atividade\nId: 1\nData e hora: 14/02/2014 20:21:21\nDura\u00E7ao: 00:00\nFrequencia Cardiaca: 0 bpm\nRepeti\u00E7oes: 0\nPeso: 0.0 kilos\nTipo de atividade: Leg press\n", string0);
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      ciclismo0.getTempo();
      assertEquals(1, ciclismo0.getCodAtividade());
      assertEquals(0, ciclismo0.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      int int0 = ciclismo0.getFreqCardiaca();
      assertEquals(0, int0);
      assertEquals(1, ciclismo0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.ofSecondOfDay(0L);
      LegPress legPress0 = new LegPress((LocalDateTime) null, localTime0, 10, 782, 782);
      int int0 = legPress0.getFreqCardiaca();
      assertEquals(1, legPress0.getCodAtividade());
      assertEquals(10, int0);
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      benchPress0.setFreqCardiaca(680);
      Period period0 = Period.ofWeeks(682);
      IsoChronology isoChronology0 = period0.getChronology();
      LocalDate localDate0 = MockIsoChronology.dateNow(isoChronology0);
      UtilizadorPraticanteOcasional utilizadorPraticanteOcasional0 = new UtilizadorPraticanteOcasional(" Com;i2]6E&M[", "Projeto.AtivRepeticoes", "4KiUr8ML>pG><l&{7qx", 4859, 682, 4859, localDate0, '');
      double double0 = benchPress0.getFatorFreqCardiaca(utilizadorPraticanteOcasional0);
      assertEquals(680, benchPress0.getFreqCardiaca());
      assertEquals(2.0, double0, 0.01);
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6652, 6652);
      LocalDate localDate0 = MockLocalDate.ofEpochDay(6652);
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador("", "", "Projeto.Atividade", (-151), 6652, 6652, localDate0, 'h');
      double double0 = corrida0.getFatorFreqCardiaca(utilizadorAmador0);
      assertEquals(1, corrida0.getCodAtividade());
      assertEquals(6652, corrida0.getFreqCardiaca());
      assertEquals((-0.8), double0, 0.01);
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      BenchPress benchPress0 = new BenchPress((LocalDateTime) null, localTime0, (-10), (-10), (-193.9));
      benchPress0.getDataRealizacao();
      assertEquals((-10), benchPress0.getFreqCardiaca());
      assertEquals(1, benchPress0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Flexoes flexoes0 = new Flexoes();
      UtilizadorProfissional utilizadorProfissional0 = new UtilizadorProfissional();
      flexoes0.setProximoCodigo(0);
      Atividade atividade0 = flexoes0.geraAtividade(utilizadorProfissional0, 2.0);
      int int0 = atividade0.getCodAtividade();
      assertEquals(1, flexoes0.getCodAtividade());
      assertEquals(0, atividade0.getFreqCardiaca());
      assertEquals(0, int0);
      assertEquals(0, flexoes0.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Flexoes flexoes0 = new Flexoes();
      UtilizadorProfissional utilizadorProfissional0 = new UtilizadorProfissional();
      flexoes0.setProximoCodigo((-11));
      Atividade atividade0 = flexoes0.geraAtividade(utilizadorProfissional0, 2.0);
      int int0 = atividade0.getCodAtividade();
      assertEquals(0, atividade0.getFreqCardiaca());
      assertEquals(0, flexoes0.getFreqCardiaca());
      assertEquals((-11), int0);
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Flexoes flexoes0 = new Flexoes();
      UtilizadorProfissional utilizadorProfissional0 = new UtilizadorProfissional();
      flexoes0.setProximoCodigo(0);
      Atividade atividade0 = flexoes0.geraAtividade(utilizadorProfissional0, 1102.9);
      assertEquals(1, flexoes0.getCodAtividade());
      assertEquals(0, flexoes0.getFreqCardiaca());
      assertEquals(0, atividade0.getFreqCardiaca());
      assertEquals(0, atividade0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Abdominais abdominais0 = new Abdominais();
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador();
      Atividade atividade0 = abdominais0.geraAtividade(utilizadorAmador0, (-1418.88542032));
      assertEquals(0, abdominais0.getFreqCardiaca());
      assertEquals(2, atividade0.getCodAtividade());
      assertEquals(0, atividade0.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6652, 6652);
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador();
      corrida0.setProximoCodigo((-1556));
      assertEquals(2, corrida0.getCodAtividade());
      assertEquals(6652, corrida0.getFreqCardiaca());
      
      Atividade atividade0 = benchPress0.geraAtividade(utilizadorAmador0, 33);
      assertEquals((-1556), atividade0.getCodAtividade());
      assertTrue(atividade0.equals((Object)benchPress0));
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      ciclismo0.equals(ciclismo0);
      assertEquals(0, ciclismo0.getFreqCardiaca());
      assertEquals(1, ciclismo0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6652, 6652);
      corrida0.equals("Projeto.Atividade");
      assertEquals(6652, corrida0.getFreqCardiaca());
      assertEquals(1, corrida0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6632, 6632);
      ZoneId zoneId0 = ZoneId.systemDefault();
      LocalDate localDate0 = MockLocalDate.now(zoneId0);
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador("", "", "", 6632, 6632, (-779), localDate0, 'G');
      double double0 = corrida0.consumoCalorias(utilizadorAmador0);
      assertEquals(1, corrida0.getCodAtividade());
      assertEquals(6632, corrida0.getFreqCardiaca());
      assertEquals(56669.63719861107, double0, 0.01);
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6652, 6652);
      LocalDate localDate0 = MockLocalDate.ofEpochDay(6652);
      UtilizadorAmador utilizadorAmador0 = new UtilizadorAmador("", "", "", (-151), 6652, 6652, localDate0, 'h');
      double double0 = corrida0.consumoCalorias(utilizadorAmador0);
      assertEquals(6652, corrida0.getFreqCardiaca());
      assertEquals((-193886.73091666674), double0, 0.01);
      assertEquals(1, corrida0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      BicepCurls bicepCurls0 = new BicepCurls();
      Instant instant0 = MockInstant.ofEpochMilli(1818L);
      ZoneOffset zoneOffset0 = ZoneOffset.MAX;
      LocalDateTime localDateTime0 = MockLocalDateTime.ofInstant(instant0, zoneOffset0);
      LegPress legPress0 = new LegPress(localDateTime0, (LocalTime) null, 1429, 1429, 2.0);
      int int0 = bicepCurls0.compareTo((Atividade) legPress0);
      assertEquals(2, legPress0.getCodAtividade());
      assertEquals(44, int0);
      assertEquals(0, bicepCurls0.getFreqCardiaca());
      assertEquals(1429, legPress0.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      BicepCurls bicepCurls0 = new BicepCurls((LocalDateTime) null, localTime0, 1417, (-987), (-987));
      // Undeclared exception!
      try { 
        bicepCurls0.toString();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      BicepCurls bicepCurls0 = new BicepCurls((LocalDateTime) null, localTime0, 1417, (-987), (-987));
      // Undeclared exception!
      try { 
        bicepCurls0.getFatorFreqCardiaca((Utilizador) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Trail trail0 = new Trail();
      // Undeclared exception!
      try { 
        trail0.geraAtividade((Utilizador) null, (-161));
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.Trail", e);
      }
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Corrida corrida0 = new Corrida((LocalDateTime) null, localTime0, 6640, 6640);
      Object object0 = corrida0.clone();
      // Undeclared exception!
      try { 
        corrida0.equals(object0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      BicepCurls bicepCurls0 = new BicepCurls((LocalDateTime) null, localTime0, 1417, (-987), (-987));
      // Undeclared exception!
      try { 
        bicepCurls0.consumoCalorias((Utilizador) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.BicepCurls", e);
      }
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      Corrida corrida0 = new Corrida();
      UtilizadorProfissional utilizadorProfissional0 = new UtilizadorProfissional();
      // Undeclared exception!
      try { 
        corrida0.consumoCalorias(utilizadorProfissional0);
        fail("Expecting exception: ArithmeticException");
      
      } catch(ArithmeticException e) {
         //
         // / by zero
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.ofSecondOfDay(0L);
      LegPress legPress0 = new LegPress((LocalDateTime) null, localTime0, 10, 782, 782);
      BenchPress benchPress0 = new BenchPress();
      // Undeclared exception!
      try { 
        legPress0.compareTo((Atividade) benchPress0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      Month month0 = Month.MARCH;
      LocalDateTime localDateTime0 = MockLocalDateTime.of(1, month0, 1, 1, 1, 1);
      Btt btt0 = new Btt(localDateTime0, (LocalTime) null, 1, 1, 1);
      btt0.getTempo();
      assertEquals(1, btt0.getFreqCardiaca());
      assertEquals(1, btt0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      Period period0 = Period.ofWeeks(682);
      IsoChronology isoChronology0 = period0.getChronology();
      LocalDate localDate0 = MockIsoChronology.dateNow(isoChronology0);
      UtilizadorPraticanteOcasional utilizadorPraticanteOcasional0 = new UtilizadorPraticanteOcasional(" Com;i2]6E&M[", "Projeto.AtivRepeticoes", "4KiUr8ML>pG><l&{7qx", 4859, 682, 4859, localDate0, '');
      // Undeclared exception!
      try { 
        benchPress0.getFatorFreqCardiaca(utilizadorPraticanteOcasional0);
        fail("Expecting exception: ArithmeticException");
      
      } catch(ArithmeticException e) {
         //
         // / by zero
         //
         verifyException("Projeto.Atividade", e);
      }
  }

  @Test(timeout = 4000)
  public void test29()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      ciclismo0.getDataRealizacao();
      assertEquals(0, ciclismo0.getFreqCardiaca());
      assertEquals(1, ciclismo0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test30()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Abdominais abdominais0 = new Abdominais((LocalDateTime) null, localTime0, 33, 6652);
      int int0 = abdominais0.getCodAtividade();
      assertEquals(33, abdominais0.getFreqCardiaca());
      assertEquals(1, int0);
  }

  @Test(timeout = 4000)
  public void test31()  throws Throwable  {
      LocalDateTime localDateTime0 = MockLocalDateTime.now();
      Corrida corrida0 = new Corrida(localDateTime0, (LocalTime) null, (-2160), 0);
      int int0 = corrida0.getFreqCardiaca();
      assertEquals((-2160), int0);
      assertEquals(1, corrida0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test32()  throws Throwable  {
      Btt btt0 = new Btt();
      btt0.setTempo((LocalTime) null);
      assertEquals(0, btt0.getFreqCardiaca());
      assertEquals(1, btt0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test33()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      Ciclismo ciclismo1 = new Ciclismo(ciclismo0);
      ZoneOffset zoneOffset0 = ZoneOffset.UTC;
      LocalDateTime localDateTime0 = MockLocalDateTime.ofEpochSecond(505, 505, zoneOffset0);
      ciclismo0.setDataRealizacao(localDateTime0);
      int int0 = ciclismo0.compareTo((Atividade) ciclismo1);
      assertEquals(1, ciclismo0.getCodAtividade());
      assertEquals((-44), int0);
      assertEquals(0, ciclismo1.getFreqCardiaca());
      assertEquals(1, ciclismo1.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test34()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      BenchPress benchPress1 = new BenchPress();
      benchPress1.setFreqCardiaca((-85));
      boolean boolean0 = benchPress1.equals(benchPress0);
      assertEquals((-85), benchPress1.getFreqCardiaca());
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void test35()  throws Throwable  {
      BenchPress benchPress0 = new BenchPress();
      BenchPress benchPress1 = new BenchPress();
      boolean boolean0 = benchPress1.equals(benchPress0);
      assertEquals(2, benchPress1.getCodAtividade());
      assertTrue(boolean0);
      assertEquals(0, benchPress1.getFreqCardiaca());
  }

  @Test(timeout = 4000)
  public void test36()  throws Throwable  {
      LocalTime localTime0 = MockLocalTime.now();
      Abdominais abdominais0 = new Abdominais((LocalDateTime) null, localTime0, 1396, 0);
      UtilizadorProfissional utilizadorProfissional0 = new UtilizadorProfissional();
      double double0 = abdominais0.consumoCalorias(utilizadorProfissional0);
      assertEquals(0.0, double0, 0.01);
      assertEquals(1396, abdominais0.getFreqCardiaca());
      assertEquals(1, abdominais0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test37()  throws Throwable  {
      Flexoes flexoes0 = new Flexoes();
      UtilizadorPraticanteOcasional utilizadorPraticanteOcasional0 = new UtilizadorPraticanteOcasional();
      Atividade atividade0 = flexoes0.geraAtividade(utilizadorPraticanteOcasional0, 1);
      atividade0.equals(flexoes0);
      assertEquals(0, atividade0.getFreqCardiaca());
      assertEquals(0, flexoes0.getFreqCardiaca());
      assertEquals(2, atividade0.getCodAtividade());
  }

  @Test(timeout = 4000)
  public void test38()  throws Throwable  {
      Ciclismo ciclismo0 = new Ciclismo();
      Ciclismo ciclismo1 = new Ciclismo(ciclismo0);
      assertTrue(ciclismo1.equals((Object)ciclismo0));
      
      ZoneOffset zoneOffset0 = ZoneOffset.UTC;
      LocalDateTime localDateTime0 = MockLocalDateTime.ofEpochSecond(505, 505, zoneOffset0);
      ciclismo0.setDataRealizacao(localDateTime0);
      boolean boolean0 = ciclismo0.equals(ciclismo1);
      assertFalse(boolean0);
  }
}
