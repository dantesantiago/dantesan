// filename: pageobjects/Base.java 
package test.java.pageobjects;

import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.*;
//import org.junit.Before;
import org.openqa.selenium.By;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class BaseWin {

  // missing lines in BootCamp Doc
  public WebDriver driver;
  
  BaseWin() {
  
      ChromeOptions chromeOptions = new ChromeOptions();
      chromeOptions.addArguments("--start-maximized");

	  String driverPath = "C:/Selenium/FirefoxDriver/";
	  System.out.println("launching Firefox browser");
	  System.setProperty("webdriver.gecko.driver", driverPath + "geckodriver.exe");
	   
	  this.driver = new FirefoxDriver(chromeOptions);

  }	
  
   public void visit(String page) {
	   driver.get(page);
   }
	
   public void click(By startButton) {
	   WebElement stButton = this.driver.findElement(startButton);
	   stButton.click();   
   }
   // missing lines in BootCamp Doc
   
	public Boolean waitForIsDisplayed(By locator, Integer... timeout) { 
	        try { 
	            waitFor(ExpectedConditions.visibilityOfElementLocated(locator), 
	                    (timeout.length > 0 ? timeout[0] : null)); 
	        } catch (org.openqa.selenium.TimeoutException exception) {
	        	 System.out.println("Web Element " + locator.toString() + " is not displayed yet!");
	             return false; 
	        } return true; 
	}
	
	// check for "clickability"
	public Boolean waitForIsClickable(By locator, Integer... timeout) { 
      try { 
            waitFor(ExpectedConditions.elementToBeClickable(locator), 
                    (timeout.length > 0 ? timeout[0] : null)); 
        } catch (org.openqa.selenium.TimeoutException exception) {
             return false; 
        } return true; 
    }
	
	public void waitFor(ExpectedCondition<WebElement> condition, Integer timeout) {
	    timeout = timeout != null ? timeout : 5;
	    WebDriverWait wait = new WebDriverWait(driver, timeout);
	    //wait.until(condition);
	}
	 	
	
	

}
