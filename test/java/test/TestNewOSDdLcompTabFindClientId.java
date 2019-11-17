// filename: tests/TestNewOSDdL.java
package test.java.tests;
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

import test.java.pageobjects.NewOSDdL;


 
public class TestNewOSDdLcompTabFindClientId {
	
  private WebDriver driver;
  private NewOSDdL newOSDdL;
  

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
  private String currSK = "";
 
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
    
     // get the total number of records - New OSD only displays 10 records at first time! Then selectable 10 20 50 MAX
     By byNumMediaIds = By.xpath( "//div[@class='mat-paginator-range-label']");
     WebElement weNumMediaIds = newOSDdL.webElementLocated(byNumMediaIds, 4);
     String numMediaIdsStr = weNumMediaIds.getText(); // 1 - 10 of 151
     String[] numMIArray = numMediaIdsStr.split(" ");
     //int maxNumMediaIds = Integer.parseInt(numMIArray[4]);
    	
     // press the arrow down to go to the next page
     By byNextPage = By.xpath("//div[@class='mat-select-arrow-wrapper']");
     WebElement weArrowDown = newOSDdL.webElementLocated(byNextPage, 2);
     newOSDdL.buttonClickable(byNextPage);
     weArrowDown.click();	
     
     // then select the last row of the menu: 10 20 50 MAX
     //By bymaxNumRows = By.id("mat-option-24"); // id changes!
     /*	By the max num rows!
     String nRVal = "'" + numMIArray[4] + "'";
     By byMaxNumRows = By.xpath("//mat-option[@ng-reflect-value=nRVal");
     */
     
     // select the max num of rows
     /*
     WebElement weMaxNumRows = newOSDdL.webElementLocated(bymaxNumRows, 2);
     newOSDdL.elementClickable(bymaxNumRows);
     weMaxNumRows.click();
     */
     
     // select by text
     /* ERROR: org.openqa.selenium.support.ui.UnexpectedTagNameException: Element should have been "select" but was "div"
     By byDropDown = By.xpath("//div[@class='mat-select-content ng-trigger ng-trigger-fadeInContent']");
     WebElement weDropDown = newOSDdL.webElementLocated(byDropDown, 4);
     Select selDropDown = new Select(weDropDown);
     selDropDown.selectByVisibleText(numMIArray[4]);
     */
     
     // data-value selection
     By byMaxNumRows = By.xpath("//mat-option[@ng-reflect-value='" + numMIArray[4] + "']");
     WebElement weMaxNumRows = newOSDdL.webElementLocated(byMaxNumRows, 4);
     weMaxNumRows.click();
     
    // Get the grid
    By byGrid = By.xpath("//mat-table[@class='table table-hover table-mc-light-blue mat-table']");
    WebElement grid = driver.findElement(byGrid);
    
    // Get all the rows
    //By locAllRows = By.xpath("//mat-row[@class='mat-row ng-star-inserted highlight']");
    //By locAllRows = By.xpath("//mat-row[@_ngcontent-c28='']");
    //By locAllRows = By.xpath("//mat-row[@class='mat-row ng-star-inserted']");
    By locAllRows = By.xpath("//mat-row[@role='row']");
    
    // dantesan--2018-03-22--HB - sometimes no rows!
    if(!newOSDdL.webElementPresent(locAllRows))
    	return false;
    
    List<WebElement> allRows = grid.findElements(locAllRows);
    int rSize = allRows.size();
    
    // Loop through each row 
    for(int i = 0; i < rSize; i++ ) {  

      WebElement gRow = allRows.get(i);
      gRow.click();
      
      //By skNum = By.xpath("//div[@class='ui-grid-cell ng-scope ui-grid-disable-selection ui-grid-coluiGrid-002Z']");
      //String skNumStr =  gRow.findElement(skNum).getText();
      //String mediaIdStr =  gRow.getText();
      
      // mediaIdStr='43100 4247085 LENA TEST 195 LenaVo 2017-11-15 12:02 PM 2017-11-15 12:14 PM OE N OK MSI195 27 9 18 7 1 6 18 0'
      // - need to split!
      
      String rowStr = gRow.getText();
      String[] rowElems = rowStr.split(" ");
      String mediaIdStr = rowElems[1];
      String sK = rowElems[0];
      int rowNum = i + 1;
      System.out.println("SK = <" + sK + "> mediaId = <" + mediaIdStr + "> Row# = " + rowNum + " of " + rSize);

      // show custom menu
      action.contextClick(allRows.get(i)).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.ARROW_DOWN).sendKeys(Keys.RETURN).build().perform();
      
      // get Client Detail Window 
      clientDetailWin = driver.getWindowHandle();
      
      System.out.println("\nClient Detail Window = |" + clientDetailWin + "|\n");
      // select Display Client Detail
      By byDispClientDtl = By.xpath("//a[@class='dropdown-item btn-secondary ng-star-inserted']"); 
      //By byDispClientDtl = By.xpath("//li[@data-action='displayClientDetail']");
      WebElement dispClientDtl = driver.findElement(byDispClientDtl);
      
      // wait for the menu to appear
      assertTrue("Custom menu did not come out!",
    		     newOSDdL.webElementPresent(byDispClientDtl));
      if(newOSDdL.buttonClickable(byDispClientDtl))
    	  dispClientDtl.click();

      if(chkClientIdInClientDtlWin(sK, mediaIdStr)) {
    	//clientIdFnd = false;
    	clientIdFnd = true;   
        break;	  
      }
    
    } // Loop through each row

    
    return(clientIdFnd);

  } // private boolean selectRow()

  //
  // returns false if client Id is not found in Client Detail Window
  //
  private boolean chkClientIdInClientDtlWin(String sK, String mediaIdStr) {
    boolean clientIdFnd = false;
    // Action object
    Actions action = new Actions(driver);
    
    this.currMediaIdStr = mediaIdStr;
    this.currSK = sK;
    
    // Get the grid
    By byGridCell = By.xpath("//div[@class='yes-scroll-table']"); 
    WebElement grid = driver.findElement(byGridCell);
    
    // Get all the rows
    //By locAllRows = By.xpath("//div[@class='ui-grid-cell-contents ng-binding ng-scope']"); // 278 rows!!!
    //BlocAllRows = By.xpath("//mat-cell[@class='mat-cell cdk-column-clientId mat-column-clientId ng-star-inserted']"); //ClientId only
    //By locAllRows = By.xpath("//mat-row[@class='mat-row ng-star-inserted']");
    By locAllRows = By.xpath("//mat-row[@_ngcontent-c28='']");
    
    // maybe so fast that the program is not able to see the row with the client Id
    //WebElement myDynamicElement = (new WebDriverWait(driver, 45))
    //	      .until(ExpectedConditions.presenceOfElementLocated(locAllRows));
    // dantesan--2018-02-23 -- This causes the test to stop if there are no client Id rows displayed!
    
    /* dantesan--2018-03-23 - comment out!
    assertTrue( "Rows of data not displayed!",
    		    newOSDdL.webElementIsLocated(locAllRows, 10));*/ 
    
    // causes error - continues search for the media Id rows even if a row does not have the clientId
    
    //if(!(clientIdFnd = newOSDdL.webElementIsLocated(locAllRows, 10))) {	// 10 secs will do!
    //	return(clientIdFnd);
    //}
    
    // dantesan--2018-03-22--HB - sometimes no rows!
    if(!newOSDdL.elementClickable(locAllRows, 2)) {
        setControlBackToMainWindow(); // remove the one in CompleteLoad()
        return(clientIdFnd);
    }
      
    
    List<WebElement> allRows = grid.findElements(locAllRows);
    int rSize = allRows.size();
    
    // Loop through each row 
    for(int i = 0; i < rSize; i++ ) {
    	
      WebElement gRow = allRows.get(i);

      String clientRowStr = gRow.getText();  
      String[] rowElems = clientRowStr.split(" ");
      String clientIdStr = rowElems[0];

      
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
      //By byCloseButtonCDW = By.xpath("//button[@class='btn-primary']");	// really bombs out!
      //By byCloseButtonCDW = By.xpath("//button[@_ngcontent-c29='']");//_ngcontent-c29 - really bombs out!
      WebElement closeBttn; // = driver.findElement(byCloseButtonCDW);
      // by button label
      //String string = String.format("//button[contains(.,'Close')]"); // same as below ... label worked!
      By byCloseButtonCDW = By.xpath("//button[contains(.,'Close')]");  // or maybe all the above work, but error was just fixed with sleepWait() - NO!
                                                                       

      
      //if(newOSDdL.buttonClickable(byCloseButtonCDW)) {
      if((closeBttn = newOSDdL.webElementLocated(byCloseButtonCDW, 30)) != null) {
        System.out.println("\nClient Detail Window still exists!\n");	
        //Implicit wait!
        //driver.manage().timeouts().implicitlyWait( 10, TimeUnit.SECONDS);
        //closeBttn = newOSDdL.fluentWait(byCloseButtonCDW);
        sleepWait(2); // 5
        closeBttn.click();
        sleepWait(2); // 5
      } else {
    	System.out.println("\nClient Detail Window CLOSED!\n"); 
      }
      //}
        
    //}
  	
    driver.switchTo().window(baseWin);
    
  } //private void setControlBackToMainWindow()
 
  private void sleepWait( int sleepSecs ){ 
    try {
        Thread.sleep(sleepSecs*1000);
    } catch (Exception e) {
     	  System.out.println("can't wait!"); //e.printStackTrace());
    }
  }
  @Before
  public void setUp() {
    newOSDdL = new NewOSDdL();
    driver = newOSDdL.OSDdlGetDriver();
  }
  @Test
  public void CompleteLoads() {
	  
    newOSDdL.loadOSD();
    
    assertTrue("Client Load History tab is not displayed!",
    	    newOSDdL.allTabsPresent());
   
    //ArrayList<String> tab = new ArrayList<String> (driver.getWindowHandles());
    //driver.switchTo().window(tab.get(0));
    
    // save the main OSD window
    baseWin = driver.getWindowHandle();
    System.out.println("\nMain OSD Window = |" + baseWin + "|\n");
    
    WebElement completedLoadsTab = driver.findElement(By.id("mat-tab-label-1-3"));
    System.out.println( "Completed Load = <" + completedLoadsTab.getText() + ">");
    completedLoadsTab.click();
    
    
    System.out.println("\nRESULT,CLIENT ID,ACTUAL RESULT,SK,MEDIA ID\n");
    
    // became class ArrayList
    //ArrayList<String> clientIdList= new ArrayList<String>(); //Creating arraylist 
    
    // get the client Ids from a file
    //getClientIdsFromFile();
    
    int ctr = 0;
    
    // 2018-02-23 - New OSD Test - media Id's with errors - ../Docs/NewOSD_TST1.csv, NewOSD_TST1.xlsx
    //
    
    
    // bombs out with this client Id
    //clientIdList.add("30048311");

    // FOUR_GOOD_DATA - GOOD to test 
    /*
    clientIdList.add("12103691");
    clientIdList.add("01109735");
    clientIdList.add("12000912");
    */
    clientIdList.add("12057693");
    

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
      //WebElement clientId = driver.findElement(By.id("clientIdInputForm"));
      //By clientIdBy = By.xpath("//input[@class='mat-input-element mat-form-field-autofill-control ng-pristine ng-valid ng-touched']");
      By clientIdBy = By.xpath("//input[@ng-reflect-placeholder='Client Id:']");
      //By clientIdBy = By.xpath("//input[@ng-reflect-id='clientIdInputForm']");
      WebElement clientId = driver.findElement(clientIdBy);
      
      WebElement frDate = driver.findElement(By.id("mat-input-12"));
      WebElement toDate = driver.findElement(By.id("mat-input-13"));
      
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
      By xpath = By.xpath("//button[@class='btn-primary']");
      
      WebElement myDynamicElement = (new WebDriverWait(driver, 45))
        .until(ExpectedConditions.presenceOfElementLocated(xpath));
      
      myDynamicElement.click();
      
      
      // If there are multiple client Id's and if one has no data, there will be error ...
      //assertTrue("Rows of qualified Loads not displayed!",
      //	    newOSDdL.skRowGridPresent());
      if(!newOSDdL.skRowGridPresent()) {
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
      	System.out.println("\n\nERROR: All SKs + media Id (" + currMediaIdStr + ") do not have the Client Id (" + clientIdStr + ").\n\n");
      	System.out.println("RESULT," + clientIdStr +", ERROR - All + Media Id does not have the client Id in all the SKs.," + currMediaIdStr);
      } else {
      	System.out.println("\n\nGOOD! A SK +  media Id's listed have the Client Id (" + clientIdStr + ").\n\n");
      	System.out.println("RESULT," + clientIdStr +", GOOD - SK (" + currSK + ") + media Id displayed have the client Id.");
      			
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
