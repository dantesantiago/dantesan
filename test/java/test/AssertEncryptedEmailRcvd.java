// filename: tests/TestNewWINdL.java
package test.java.test;
import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.List;
import java.util.Scanner;
import java.util.Iterator;

// read clientIds from a file
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;



import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import test.java.pageobjects.NewWindL;


 
public class AssertEncryptedEmailRcvd {
	
  private WebDriver driver;
  private NewWindL newWINdL;
  private static String encrpEmSubj = "Virtru Encrypted Email Send Test";
  private static String emBodySent  = "Test encrypted e-mail sent!";
  


  
  private String baseWin;
  private String clientDetailWin;
 
  private void sleepWait( int sleepSecs ){ 
	  try {
		  	Thread.sleep(sleepSecs*1000);
	  } catch(Exception e) {
		  System.out.println("can't wait!"); //e.printStackTrace());
	  }
  }
  
  // Select the encrypted email from the unread list ...
  private void selectEmail(String emailSubj, String dispMsg) {
	  
	    System.out.println("\n" + dispMsg + "\n");
	    System.out.println("Going through e-mail list ...");
	    List<WebElement> email = driver.findElements(By.cssSelector("div.xT>div.y6>span>b"));

	    for(WebElement emailsub : email){
	      System.out.println("Email Subj: <" + emailsub.getText() + ">");
	      if(emailsub.getText().contains(emailSubj) == true){
	        emailsub.click();
	      break;
	      }
	    }
  }
  
  //press Button
  private void pressBttn(String buttonClass, String actionMsg) {
	  
	  System.out.println(actionMsg);
	  
	  By byClassBttn = By.className(buttonClass);
	  WebElement WElemBttn = newWINdL.webElementLocated(byClassBttn, 10);
	  WElemBttn.click();
  }
  
  // go to next tab
  private void goToNextTab() {
	  String subWindowHandler = null;
	  Set<String> handles = driver.getWindowHandles(); // get all window handles
	              Iterator<String> iterator = handles.iterator();
	              while (iterator.hasNext()){
	                  subWindowHandler = iterator.next();
	              }
	  driver.switchTo().window(subWindowHandler); // switch to popup window
  }
  
  @Before
  public void setUp() {
    newWINdL = new NewWindL();
    driver = newWINdL.WINdlGetDriver();
  }
  @Test
  public void VerifyEncryptedEmail() {
	  
    newWINdL.loadWIN();
    
    String parentWindowHandler=driver.getWindowHandle();// parent window

    sleepWait(30); // 60
    
    selectEmail(encrpEmSubj, "Find the encrypted email received ...");
    
    sleepWait(15);
    
    String uMclassStr = "CToWUd";
    String actionMsg = "Press the 'Unlock Message' button ...";
    pressBttn(uMclassStr, actionMsg);
    
    // Press the user email address
    goToNextTab();
    sleepWait(15);
    String userEmClassStr = "userEmail";
    actionMsg = "Press the user email address button ...";
    pressBttn(userEmClassStr, actionMsg);    
    
    // Press 'Send Verification E-mail'
    sleepWait(15);
    String sndVerEmailClassStr = "btn btn-lg auth-choice-btn sendEmailButton";
    actionMsg = "Press the 'Send Verification Email' button ...";
    pressBttn(sndVerEmailClassStr, actionMsg);    
    
    // go back to e-mail list - press Inbox
    
    // Find the verification email and click
    
    //Press the 'Unlock Message' button ...
    
    
    // Assert the email message
    sleepWait(15); // 30
    System.out.println("Display the verification email ...");

    
    
  }
  
  @After
  public void tearDown() throws Throwable {		
	System.out.println("Firefox window will be closed in 10 secs ...");
	sleepWait(10);
  	super.finalize();
  	driver.quit();
  }
}
