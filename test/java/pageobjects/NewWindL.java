//filename: pageobjects/NewWINdL.java 
package test.java.pageobjects;
import java.util.NoSuchElementException;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

//import com.google.common.base.Function;

import org.openqa.selenium.WebDriver.Timeouts;

public class NewWindL extends BaseWin {
  
  // Inbox link
  By byInbox = By.className("TO nZ aiq");

  WebDriver WINdlWD;
    
  public NewWindL() {
	  super();
	  WINdlWD = super.driver;
  }
  
  public WebDriver WINdlGetDriver() {
	  return(WINdlWD);
  }
  
  public void loadWIN() {
	 
     visit("https://mail.google.com/");  
  }
  
  public Boolean inboxDisplayed() {
    return waitForIsDisplayed(byInbox, 240 ); 
  }
  
  // wait method for the given Web Element
  public Boolean webElementPresent(By byWebElem) {
	    return waitForIsDisplayed(byWebElem, 60);  //1 min
  }
  
  //wait method for the button to be clickable
  public Boolean buttonClickable(By byButton) {
	  return waitForIsClickable(byButton, 30);
  }
  
  //wait method for the element to be clickable
  public Boolean elementClickable(By byButton, int secs) {
	  return waitForIsClickable(byButton, secs);
  }
  
  // Wait for the WebElement to be located
  // returns true - if WebElement is located
  //         false - if not
  // dantesan--2018-05-31 - .until error fixed by standalone server jar 
  //                         selenium-server-standalone-3.12.0.jar
  public Boolean webElementIsLocated(By byXpath, Integer waitSecs) {

	  WebElement myDynamicElement = (new WebDriverWait(driver, waitSecs))
		      .until(ExpectedConditions.presenceOfElementLocated(byXpath));
	  if(myDynamicElement != null )
		  return true;
	  else
		  return false;
	  
  }

  // Wait for the WebElement to be located
  // returns the WebElement whether null or not
  public WebElement webElementLocated(By byXpath, Integer waitSecs) {
	  WebElement myDynamicElement = (new WebDriverWait(driver, waitSecs))
		      .until(ExpectedConditions.presenceOfElementLocated(byXpath));
	  return (myDynamicElement);

  }	   

}
