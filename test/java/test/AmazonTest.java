//filename: tests/AmazonTest.java
package test.java.tests;

import org.junit.After;
import org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import test.java.pageobjects.AmazonPage;

//import org.openqa.selenium.chrome.ChromeDriver;
public class AmazonTest {
    private WebDriver driver;
    private AmazonPage amznPage;
    String winHandleBefore;
    @Before
    public void setUp() {
        System.setProperty("webdriver.gecko.driver","C:\\Selenium\\Automation\\drivers\\geckodriver.exe");
        //DesiredCapabilities capabilities = DesiredCapabilities.firefox();
        //capabilities.setCapability("marionette",true);
        driver = new FirefoxDriver();
        //comment the above 2 lines and uncomment below 2 lines to use Chrome
        //System.setProperty("webdriver.chrome.driver","D:\\Automation\\drivers\\chromedriver.exe");
        //WebDriver driver = new ChromeDriver();
        amznPage = new AmazonPage(driver);
        winHandleBefore = driver.getWindowHandle();
    }

    // Test Case 1: 'Press Help' and then press 'Manage Prime'
    @Test
    public void test01_managePrime() {
        System.out.println("\n\nHELP + managePrime");
        amznPage.pressHelp();
        amznPage.pressManagePrime();
        //tearDown();
    }

    // Test Case 2:
    //   a. 'Press Help' and DgtlSvcsAndDvcSpprt
    //   b. Validate that Amazon Digital Services and Device Support are displayed on the page
    //   c. Click on the image for �Echo Family' and then 'Echo Dot�
    @Test
    public void test02_dgtlSvcsAndDvcSpprt() {
        System.out.println("\n\nDigital Services and Device Support");
        driver.switchTo().window(winHandleBefore);
        amznPage.pressHelp();
        amznPage.pressDgtlSvcsAndDvcSpprtImg();
        amznPage.validateDgtlSvcsAndDvcSpprtPage();
        amznPage.pressEchoFamilyThenEchoDot();
        amznPage.validateEchoDotSupprt();
    }

    // Test Case 3:
    //   a. In the �Search Help� textbox in the left-hand-side of the page,
    //          enter �Samsung TV� and click on the Go button next to it
    //   b. Close browser
    @Test
    public void test03_SamsungTV_search() {
        System.out.println("\n\nSearch \"Samsung TV\"");
        driver.switchTo().window(winHandleBefore);
        amznPage.searchSite("Samsung TV");
    }

    @After
    public void tearDown() {
        driver.quit();
    }
}

