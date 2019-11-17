//filename: tests/TestOSD.java
package test.java.tests;
import java.util.ArrayList;
 
 import java.util.Timer;
 import java.util.TimerTask;
 
 import org.junit.Test;
 import org.junit.Before;
 import org.junit.After;
 import org.openqa.selenium.By;
 
 import org.openqa.selenium.WebDriver;
 import org.openqa.selenium.chrome.ChromeDriver;
 import org.openqa.selenium.ie.InternetExplorerDriver;
 import org.openqa.selenium.firefox.FirefoxDriver;
 
import org.openqa.selenium.interactions.Actions; 
import org.openqa.selenium.WebElement;
 
 
 import org.openqa.selenium.Keys;
 
 
 import org.openqa.selenium.support.ui.WebDriverWait;
 import org.openqa.selenium.support.ui.ExpectedConditions;
 import org.openqa.selenium.support.ui.*;
 
 
public class TestOSD {
	   
//  class RemindTask extends TimerTask {
//      public void run() {
//        System.out.println("Time's up!");
//        //toolkit.beep();
//        //timer.cancel(); //Not necessary because we call System.exit
//        //System.exit(0); //Stops the AWT thread (and everything else)
//      }
//   }
  
   public class Reminder {
       Timer timer;

       public Reminder(int seconds) {
           timer = new Timer();
           timer.schedule(new RemindTask(), seconds*1000);
   	   }

       class RemindTask extends TimerTask {
           public void run() {
               System.out.println("Time's up!");
               timer.cancel(); //Terminate the timer thread
           }
       }

   }  

   private WebDriver driver;
   private String mediaIdStr;
   private String clientIdStr = "12129119"; // "30056976";  // Media Id = 7771717
   private String frDateStr = "2017/12/01";
   private String toDateStr = "2017/12/01";
    
    
  @Before
     public void setUp() {
         //driver = new FirefoxDriver();
        
	   // ERROR: rg.openqa.selenium.SessionNotCreatedException: Unexpected error launching Internet Explorer. Browser zoom level was set to 125%. It should be set to 100%
  	   //driver = new InternetExplorerDriver();
	  
  	   String driverPath = "C:/Selenium/ChromeDriver/";
         System.out.println("launching Chrome browser");
         System.setProperty("webdriver.chrome.driver", driverPath+"chromedriver.exe");
  	  //driver = new ChromeDriver();
      driver = new FirefoxDriver();
  }
  @Test
     public void completedLoad() {
      driver.get("https://gtsacptlb-0188.vsp.com/OSD/#/");
      
      // does not work!
      //Timer timer = new Timer();
      //timer.schedule( new RemindTask(), 30 * 10000 );
      
      new Reminder(30);

      ArrayList<String> tab = new ArrayList<String> (driver.getWindowHandles());
      driver.switchTo().window(tab.get(0));
      WebElement completedLoadsTab = driver.findElement(By.id("ui-id-3"));
      System.out.println( "Completed Load = <" + completedLoadsTab.getText() + ">");
      completedLoadsTab.click();
      
      System.out.println( "ClientId = <" + clientIdStr + "> From Date = <" + frDateStr + "> To Date = <" + toDateStr + "> ");
      
      // get client Id, From, and To
      WebElement clientId = driver.findElement(By.name("completedLoad_clientId"));
      WebElement frDate = driver.findElement(By.name("completedLoad_from"));
      WebElement toDate = driver.findElement(By.name("completedLoad_to"));
      
      // Action object
      Actions action= new Actions(driver);
      
      // clear text boxes
      frDate.clear();
      toDate.clear();
      clientId.clear();
      action.click();
      
      
      // input the client Id     
      clientId.sendKeys(clientIdStr);
      
      // add From date 
      frDate.sendKeys(frDateStr); 
       
     // add From date
      toDate.sendKeys(toDateStr); 
      
      
      
    
      // click Refresh Data
      By byRB = By.id("refreshButton");
      WebElement refreshButton = driver.findElement(byRB);
      //WebDriverWait wait = new WebDriverWait(driver, 10);
      //WebElement refreshButton = wait.until(ExpectedConditions.presenceOfElementLocated(byRB));
//       below hangs!
//      while(true) {
//    	  if(refreshButton.isDisplayed() && refreshButton.isEnabled()) {
//    		break;  
//    	  }    		  
//      }
      //new WebDriverWait(driver, TimeSpan.FromSeconds(10)).Until(ExpectedConditions.elementIfVisible("your selector"); 
      //WebElement refreshButton = driver.findElement(By.cssSelector(".btn.btn-primary"));
      //WebElement refreshButton = driver.findElement(By.cssSelector("input[type='button']"));
      
      
      //refreshButton = driver.findElement(byRB);
      if(refreshButton.isDisplayed() )
    	  System.out.println("\"Refresh Button\" is displayed!\n");
      if(refreshButton.isEnabled() )
    	  System.out.println("\"Refresh Button\" is Enabled!\n");
      else
    	  System.out.println("\"Refresh Button\" is DISABLED!!\n");
      
      
      
      // org.openqa.selenium.ElementNotVisibleException: element not visible
      //action.doubleClick(refreshButton).perform();
      //refreshButton.click();  // org.openqa.selenium.ElementNotInteractableException: 

      
      // select grid value
      //WebElement gridValue = driver.findElement(By.cssSelector("ui-grid-row.ng-scope.ui-grid-row-selected"));
      WebElement gridValue = driver.findElement(By.id("media_7771717"));
      
      gridValue.click();
      
      // show custom menu
      
      action.contextClick(gridValue).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.RETURN).build().perform();
      
     // select Display Client Detail
      WebElement dispClientDtl = driver.findElement(By.id("openMediaIdInMob")); 
      dispClientDtl.click();
      
      
      //driver.findElement(By.id("username")).sendKeys("dantsa");
      //driver.findElement(By.id("password")).sendKeys("Mazda@23");
      //driver.findElement(By.id("signon")).submit();
      //driver.findElement(By.id("tabCompletedLoads")).submit();
      //ArrayList<String> tabs2 = new ArrayList<String> (driver.getWindowHandles());
      //driver.switchTo().window(tabs2.get(1));
      //driver.close();
      //driver.switchTo().window(tabs2.get(0));
      
      // locate using li tag - python
      /*
      li_list = driver.find_elements_by_tag_name('li')
      for li in li_list:
    	if li.get_attribute('data-title') == '<wanted_value>':
    	  <do_your_thing>
      */
  }
  /*
  @After
     public void tearDown() {
      driver.quit();
  }
  */
  

} // public class TestOSD 
