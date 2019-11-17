// filename: tests/TestLogin.java
 package test.java.tests;
 import org.junit.Test;
 import org.junit.Before;
 import org.junit.After;
  import static org.junit.Assert.*;
 import org.openqa.selenium.WebDriver;
 import org.openqa.selenium.firefox.FirefoxDriver;
 import test.java.pageobjects.Login;
   public class TestLogin {
      private WebDriver driver;
      private Login login;
    @Before
       public void setUp() {
           driver = new FirefoxDriver();
           login = new Login(driver);
    }
    @Test
       public void succeeded() {
         login.with("tomsmith", "SuperSecretPassword!");
        assertTrue("success message not present",
                login.successMessagePresent());
      }
    
    @Test
        public void failed() {
            login.with("tomsmith", "bad password");
           assertTrue("failure message wasn't present after providing bogus credentials",
                   login.failureMessagePresent());
       }
 
   
//    @After
//       public void tearDown() {
//        driver.quit();
//    }
}




////-------------------------------------------------------------
////filename: tests/TestLogin.java
// package test.java.tests;
// import org.junit.Test;
// import org.junit.Before;
// import org.junit.After;
// import org.openqa.selenium.By;
// import org.openqa.selenium.WebDriver;
// import org.openqa.selenium.firefox.FirefoxDriver;
// 
// import static org.junit.Assert.*;
// 
//   public class TestLogin {
//      private WebDriver driver;
//    @Before
//       public void setUp() {
//           driver = new FirefoxDriver();
//    }
//    @Test
//       public void succeeded() {
//        driver.get("http://the-internet.herokuapp.com/login");
//        //driver.get("file:///C:/Users/dantsa/Documents/Utils/Selenium/Login.html");
//        driver.findElement(By.id("username")).sendKeys("tomsmith");
//        driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
//        driver.findElement(By.id("login")).submit();
//        
//       assertTrue( "success message not present", driver.findElement(By.cssSelector(".flash.success1")).isDisplayed());
//    }
//    /*
//    @After
//       public void tearDown() {
//        driver.quit();
//    }
//    */
//}