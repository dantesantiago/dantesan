// filename: tests/TestOSDdynamicLoading.java
package test.java.tests;
import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
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

import org.openqa.selenium.support.ui.WebDriverWait;

import test.java.pageobjects.OSDdynamicLoading;


 
public class TestOSDdynamicLoading {
	
  private WebDriver driver;
  private OSDdynamicLoading dynamicLoading;
  

  private String mediaIdStr;								// no rows
  private String clientIdStr = "42130001"; //"12129119";//"30042795"; //"30056976"; // "30016907";  // Media Id = 7771717 
  private String frDateStr = "2017/01/01"; //"2017/12/01";
  private String toDateStr = "2017/12/31"; //"2017/12/13";
  
  private String baseWin;
  private String clientDetailWin;
  // get the current window after checking the rows in the main OSD 
  // or when there is a client Id not in the media Id displayed
  private String currWin;
  
  private String currMediaIdStr = ""; 
 
  // read client Ids from a file
  //private String clientIdFN = "../data/clientIds.txt";
  private String dataPath = "C:\\Apps\\workspace\\Selenium\\data\\";
  private String clientIdFN = dataPath + "clientIds.txt";
  //private StringBuffer clientIdsStrBuffer = new StringBuffer();
  ArrayList<String> clientIdList = new ArrayList<String>(); //Creating arraylist 
  

  // Read the client Ids from a file
  private void getClientIdsFromFile() {
		try {
			File file = new File(clientIdFN);
			FileReader fileReader = new FileReader(file);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			//StringBuffer clientIdsStrBuffer = new StringBuffer();
			String line;
			while ((line = bufferedReader.readLine()) != null) {
				//clientIdsStrBuffer.append(line);
				//clientIdsStrBuffer.append("\n");
				clientIdList.add(line.trim());
			}
			fileReader.close();
			//System.out.println("Contents of file:");
			//System.out.println(clientIdStrBuffer.toString());
		} catch (IOException e) {
			e.printStackTrace();
		}
  }

  //
  // returns false if client Id is not found in Client Detail Window
  //
  private boolean selectRow() {
    
	  boolean clientIdFnd = true;  
	  // Action object
    Actions action= new Actions(driver);
    

   

    
    // Get the grid
    By byGrid = By.xpath("//div[@role='rowgroup']");
    WebElement grid = driver.findElement(byGrid);
    
    // Get all the rows
    By locAllRows = By.xpath("//div[@class='ui-grid-cell ng-scope ui-grid-disable-selection ui-grid-coluiGrid-0030']");
    List<WebElement> allRows = grid.findElements(locAllRows);
    int rSize = allRows.size();
    
    // Loop through each row 
    for(int i = 0; i < rSize; i++ ) {  

      WebElement gRow = allRows.get(i);
      gRow.click();
      
      //By skNum = By.xpath("//div[@class='ui-grid-cell ng-scope ui-grid-disable-selection ui-grid-coluiGrid-002Z']");
      //String skNumStr =  gRow.findElement(skNum).getText();
      String mediaIdStr =  gRow.getText();
      //System.out.println("mediaId = <" + mediaIdStr + ">");

      // show custom menu
      action.contextClick(allRows.get(i)).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.RETURN).build().perform();
      
      // get Client Detail Window 
      clientDetailWin = driver.getWindowHandle();
      
      System.out.println("\nClient Detail Window = |" + clientDetailWin + "|\n");
      // select Display Client Detail
      By byDispClientDtl = By.xpath("//li[@ng-if='showDisplayGISClientDetailMenu']"); 
      //By byDispClientDtl = By.xpath("//li[@data-action='displayClientDetail']");
      WebElement dispClientDtl = driver.findElement(byDispClientDtl);
      
      // wait for the menu to appear
      assertTrue("Custom menu did not come out!",
    		     dynamicLoading.webElementPresent(byDispClientDtl));
      
      dispClientDtl.click();

      if(!chkClientIdInClientDtlWin(mediaIdStr)) {
    	clientIdFnd = false;
        break;	  
      }
    
    }
    
    return(clientIdFnd);

  } // private boolean selectRow()

  //
  // returns false if client Id is not found in Client Detail Window
  //
  private boolean chkClientIdInClientDtlWin(String mediaIdStr) {
    boolean clientIdFnd = false;
    // Action object
    Actions action = new Actions(driver);
    
    currMediaIdStr = mediaIdStr;
    
    // Get the grid
    By byGridCell = By.xpath("//div[@role='gridcell']"); // 278 rows!!!
    WebElement grid = driver.findElement(byGridCell);
    
    // Get all the rows
    //By locAllRows = By.xpath("//div[@class='ui-grid-cell-contents ng-binding ng-scope']"); // 278 rows!!!
    By locAllRows = By.xpath("//div[@class='ui-grid-cell ng-scope ui-grid-coluiGrid-005C']");
    
    // maybe so fast that the program is not able to see to row with the client Id
    //WebElement myDynamicElement = (new WebDriverWait(driver, 45))
    //	      .until(ExpectedConditions.presenceOfElementLocated(locAllRows));
    // dantesan--2018-02-23 -- This causes the test to stop if there are no client Id rows displayed!

    assertTrue( "Rows of data not displayed!",
    		    dynamicLoading.webElementIsLocated(locAllRows, 45)); 
    /*
    if(!(clientIdFnd = dynamicLoading.webElementIsLocated(locAllRows, 10))) {	// 10 secs will do!
    	return(clientIdFnd);
    }
    */
    
    
    
    List<WebElement> allRows = grid.findElements(locAllRows);
    int rSize = allRows.size();
    
    // Loop through each row 
    for(int i = 0; i < rSize; i++ ) {
    	
      WebElement gRow = allRows.get(i);

      String clientIdStr =  gRow.getText();  

      
      System.out.println("mediaId = |" + mediaIdStr + "|      |      clientId = |" + clientIdStr.trim() + "|");
      if(clientIdStr.trim().equals(this.clientIdStr.trim())) {
    	//System.out.println("mediaId = |" + mediaIdStr + "|      |      clientId = |" + clientIdStr.trim() + "|");
        clientIdFnd = true;
        //setControlBackToMainWindow();
        break;
      }
    }
	
    //if(!clientIdFnd) 
    	//System.out.println("mediaId = |" + mediaIdStr + "|      |      clientId = |" + clientIdStr.trim() + "| -- WRONG!");
    
    setControlBackToMainWindow(); // remove the one in CompleteLoad()
    return(clientIdFnd);

  } // private boolean chkClientIdInClientDtlWin(String mediaIdStr)
  
  // return control to main OSD windows
  private void setControlBackToMainWindow() {
	  /*  
    Set <String> set = driver.getWindowHandles();
    
    set.remove(baseWin);
    //set.remove(clientDetailWin); // This is removed!
    //assert set.size()==1;
    
    String currWin = set.toString();
    //driver.switchTo().window(set.toArray(new String[0]));
    driver.switchTo().window(currWin);
    
    driver.close();
    Just switchback to OSD main windows!*/
    //driver.switchTo().window(clientDetailWin);// This is removed!
	
	// get the current window displayed
	//currWin = driver.getWindowHandle();  
    // check if the Window still exists
	/*
    if(clientDetailWin.equals(currWin)) {
    */
      // press the X button of Client Detail Window
      //By byCloseButtonCDW = By.id("ui-id-18");  // wrong id!
      By byCloseButtonCDW = By.xpath("//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close']");
      WebElement closeBttn; // = driver.findElement(byCloseButtonCDW);

      if((closeBttn = dynamicLoading.webElementLocated(byCloseButtonCDW, 5)) != null) {
        System.out.println("\nClient Detail Window still exists!\n");	  
        closeBttn.click(); 	  
    	  
      } else {
    	System.out.println("\nClient Detail Window CLOSED!\n"); 
      }
        
    //}
  	
    driver.switchTo().window(baseWin);
    
  } //private void setControlBackToMainWindow()
 
  
  
  @Before
  public void setUp() {
    dynamicLoading = new OSDdynamicLoading();
    driver = dynamicLoading.OSDdlGetDriver();
  }
  @Test
  public void CompleteLoads() {
	  
    dynamicLoading.loadOSD();
    
    assertTrue("Client Load History tab is not displayed!",
    	    dynamicLoading.allTabsPresent());
   
    //ArrayList<String> tab = new ArrayList<String> (driver.getWindowHandles());
    //driver.switchTo().window(tab.get(0));
    
    // save the main OSD window
    baseWin = driver.getWindowHandle();
    System.out.println("\nMain OSD Window = |" + baseWin + "|\n");
    
    WebElement completedLoadsTab = driver.findElement(By.id("ui-id-3"));
    System.out.println( "Completed Load = <" + completedLoadsTab.getText() + ">");
    completedLoadsTab.click();
    
    
    System.out.println("\nRESULT,CLIENT ID,ACTUAL RESULT, MEDIA ID\n");
    
    // became class ArrayList
    //ArrayList<String> clientIdList= new ArrayList<String>(); //Creating arraylist 
    
    // get the client Ids from a file
    getClientIdsFromFile();
    
    int ctr = 0;
    
    // 2018-02-23 - New OSD Test - media Id's with errors - ../Docs/NewOSD_TST1.csv, NewOSD_TST1.xlsx
    //
    /*
    clientIdList.add("01109735");
    clientIdList.add("12000912");
    clientIdList.add("12057693");
    */
    // ClientId 
    
    /*
    clientIdList.add("12129119");
    clientIdList.add("30016907");
    clientIdList.add("30001265");
    
    int numClientIds = clientIdList.size();
    int ctr = 0;
    */
    
    /* v24
    clientIdList.add("30059425");
    clientIdList.add("30059426");
    clientIdList.add("30061123");
    clientIdList.add("30063291");
    clientIdList.add("30071113");
    clientIdList.add("30075713");
    clientIdList.add("30078690");
    clientIdList.add("30310000");
    clientIdList.add("30940000");
    clientIdList.add("31590000");
    clientIdList.add("32230000");
    clientIdList.add("32400000");
    clientIdList.add("32440000");
    clientIdList.add("32460000");
    clientIdList.add("34787771");
    
    v23
    clientIdList.add("12317771");
    clientIdList.add("12320000");  
    clientIdList.add("12345678");  
    clientIdList.add("12349876");  
    clientIdList.add("12862001");  
    clientIdList.add("12862005");  
    clientIdList.add("12880000");  
    clientIdList.add("13470001");  
    clientIdList.add("13940000");  
    clientIdList.add("14340000");  
    clientIdList.add("14350000"); 
    
    clientIdList.add("10140000");
    clientIdList.add("11120000");
    clientIdList.add("11910000");
    clientIdList.add("12000912");
    clientIdList.add("12002707");
    clientIdList.add("12003253");
    clientIdList.add("12010001");
    clientIdList.add("12020000");
    clientIdList.add("12020005");
    clientIdList.add("12020007");
    clientIdList.add("12020010");
    */

    int numClientIds = clientIdList.size();
    
    Iterator iter = clientIdList.iterator();
    
    while(iter.hasNext()) {
    	
      	
      clientIdStr = iter.next().toString();
      
      ctr++;
      
      System.out.println("\n" + ctr + " of " + numClientIds + " ________________________________________________________________________________\n");
      System.out.println( "\nClientId = <" + clientIdStr + "> From Date = <" + frDateStr + "> To Date = <" + toDateStr + ">\n");
      
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
      
      //WebElement refreshButton = driver.findElement(By.id("refreshButton")); // Element not Found!
      // org.openqa.selenium.NoSuchElementException: no such element: 
      // Unable to locate element: {"method":"tag name","selector":"ng-disabled"}
      //refreshButton = driver.findElement(By.tagName("ng-disabled")); 
  //    if(refreshButton.isDisplayed() )
  //  	  System.out.println("\"Refresh Button\" is displayed!\n");
  //    if(refreshButton.isEnabled() )
  //  	  System.out.println("\"Refresh Button\" is Enabled!\n");
  //    else
  //  	  System.out.println("\"Refresh Button\" is DISABLED!!\n");    
      // org.openqa.selenium.ElementNotVisibleException: element not visible
      //action.doubleClick(refreshButton).perform();
      //refreshButton.click();
  
      // click Refresh Data MANUALLY!
      //System.out.println( "\n\nPlease press \"Refresh Data\" Button\n\n" );
      
      /*
      // wait for the Refresh Button to be clickable!
      By byRefreshButton = By.id("refreshButton");
      
      // check "Refresh Button" if clickable
      
      assertTrue("Refresh Button cannot be clicked!",
      		dynamicLoading.buttonClickable(byRefreshButton));
      
      WebElement refreshButton = driver.findElement(byRefreshButton);
      refreshButton.click();
      */
      //By xpath = By.xpath("//button[@name='submit'][@type='submit'][contains(text(),'Refresh Data')]");
      //By xpath = By.xpath("//button[contains(text(),'Refresh Data')]");
      By byRefreshButton = By.id("refreshButton");
      
      By xpath = By.xpath("//button[@ng-click='searchData()']");
      
      WebElement myDynamicElement = (new WebDriverWait(driver, 45))
        .until(ExpectedConditions.presenceOfElementLocated(xpath));
      
      myDynamicElement.click();
      
      
      // If there are multiple client Id's and if one has no data, there will be error ...
      //assertTrue("Rows of qualified Loads not displayed!",
      //	    dynamicLoading.skRowGridPresent());
      if(!dynamicLoading.skRowGridPresent()) {
    	  System.out.println("\nINFO: No media Id found for this client Id (" + clientIdStr + ")!\n");
    	  System.out.println("RESULT," + clientIdStr +", INFO - No media Id found!");
    	  continue;
      }
  
      
      /*
      // select grid value
      //WebElement gridValue = driver.findElement(By.cssSelector("ui-grid-row.ng-scope.ui-grid-row-selected"));
      //WebElement gridValue = driver.findElement(By.id("media_7771717"));
      // cssSelector - unable to find element!
      //By byMediaId = By.cssSelector("ui-grid-cell ng-scope ui-grid-disable-selection ui-grid-coluiGrid-0030");
      // XPath
      By byMediaId = By.xpath("//div[@class='ui-grid-cell ng-scope ui-grid-disable-selection ui-grid-coluiGrid-0030']");
      WebElement gridValue = driver.findElement(byMediaId);   
      gridValue.click();
      // show custom menu
      action.contextClick(gridValue).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.RETURN).build().perform();
      // Go to the Menu
      By byDispClientDtl = By.xpath("//li[@ng-if='showDisplayGISClientDetailMenu']");
      WebElement dispClientDtl = driver.findElement(byDispClientDtl);
      dispClientDtl.click();
      */
  
      if(!selectRow()) {
      	System.out.println("\n\nERROR: A media Id (" + currMediaIdStr + ") that does not have the Client Id (" + clientIdStr + ") is included in the list.\n\n");
      	System.out.println("RESULT," + clientIdStr +", ERROR - Media Id does not have the client Id.," + currMediaIdStr);
      } else {
      	System.out.println("\n\nGOOD! All media Id's listed have the Client Id (" + clientIdStr + ").\n\n");
      	System.out.println("RESULT," + clientIdStr +", GOOD - All media Id's displayed have the client Id.");
      }
      
      

      
      // This will require user intervention for every good or bad result.
      /*
      Scanner reader = new Scanner(System.in);  // Reading from System.in
      System.out.println("\nSelect this Console and press 'Enter' key to end test for this clientId...\n");
      reader.nextLine();
      */

   	  // get the current window displayed
      
      //Set<String> currWins = driver.getWindowHandles();  
   	  //System.out.println("\nNumber of Windows = |" + currWins.size() + "|\n");

      // check if the Window still exists
      //if(currWins.size() > 1) {
    	//setControlBackToMainWindow(); 
      //}
    } // while(iter.hasNext())
    
    System.out.println("\n________________________________________________________________________________\n");
    System.out.println("All client Id's checked in Complete Load tab results.\n");
    System.out.println("Copy Console and grep Result (all-caps) and save in a CSV file to see test report.\n\n");
    
    
      
     // select Display Client Detail
     //WebElement dispClientDtl = driver.findElement(By.linkText("Display Client Detail"));  
     //
      // select Open Media Id in MOB and it does!
      //WebElement dispClientDtl = driver.findElement(By.id("openMediaIdInMob")); 
      //dispClientDtl.click();
    
  }
  @After
  public void tearDown() throws Throwable {		
  	super.finalize();
  	driver.quit();
  }
}
