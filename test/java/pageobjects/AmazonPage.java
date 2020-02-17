package test.java.pageobjects;

import org.junit.*;

import static org.junit.Assert.assertTrue;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.util.List;

public class AmazonPage {
    private WebDriver driver;   
    
    

    public AmazonPage(WebDriver driver) {
        this.driver = driver;
        driver.get("https://www.amazon.com/");

    }
    
    // private void sleepWait( int sleepSecs ){
    public void sleepWait( int sleepSecs ){
       try {
            Thread.sleep(sleepSecs*1000);
        } catch (Exception e) {
         	  System.out.println("can't wait!"); //e.printStackTrace());
        }
    }

    public void pressHelp() {
    	By helpLocator = By.xpath("//a[text()='Help']");
    	System.out.println("HELP = " + webElementIsLocated(helpLocator, 1) + "\n\n");
        assertTrue(webElementIsLocated(helpLocator, 1));
        driver.findElement(helpLocator).click();   
    }
    
    public void pressManagePrime() {
    	// Some things YCDH have same 'class' ...
    	By somethings = By.xpath("//h3[@class='a-spacing-none a-text-normal']");
    	List<WebElement> somethingsElements = driver.findElements(somethings);
    	for(int i=0; i<somethingsElements.size(); i++){
            if( i == 3) { // Manage Prime is fourth element ...
            	somethingsElements.get(i).click(); 
            	break;
            }       	   
    	}
        //verify Sign-in page appears
        By signInLocator = By.xpath("//h1[@class='a-spacing-small']");
        assertTrue(webElementIsLocated(signInLocator, 1));
        sleepWait(2);
    }
    
    public void pressDgtlSvcsAndDvcSpprtImg() {
    	// Some things YCDH Images have same 'class' ...
    	By somethingsImgs = By.xpath("//img[@class='ss-v2-box-image']");
    	List<WebElement> somethingsImgsElements = driver.findElements(somethingsImgs);
    	for(int i=0; i<somethingsImgsElements.size(); i++){
            if( i == 2) { // DgtlSvcsAndDvcSpprt is 3rd element ...
            	somethingsImgsElements.get(i).click(); 
            	break;
            }
    	}
    	sleepWait(2);
    }
    
    public void validateDgtlSvcsAndDvcSpprtPage() {
    	// verify heading
    	By dSADSheadingLocator = By.xpath("//h1[@class='h1headding']"); // .. some typo ...
    	assertTrue(webElementIsLocated(dSADSheadingLocator, 1));
    	System.out.println("Digital Services and Device Support ... page displayed ...");
    	// Other labels that exist can be verified ...
    	sleepWait(2);
    }
    
    public void pressEchoFamilyThenEchoDot() {
       By echoFamilyImgLocator = By.xpath("//img[@class='devicepickeroptionimg']");	
       assertTrue(webElementIsLocated(echoFamilyImgLocator, 1));
       // click it
       driver.findElement(echoFamilyImgLocator).click(); 
       System.out.println("Echo Family is selected!");
       sleepWait(2);
       // press Echo Dot
       By echoDotLocator = By.linkText("Echo Dot");
       driver.findElement(echoDotLocator).click();
       System.out.println("Echo Dot pressed!");
       sleepWait(2);
    	
    }
    
    public void validateEchoDotSupprt() {
        // Echo Dot Support main image
        By echoDotSpprtMainImgLocator = By.xpath("//img[@alt='Support for Echo Dot']");
        assertTrue(webElementIsLocated(echoDotSpprtMainImgLocator, 1));
        System.out.println("Echo Dot Support page verified as displayed!\n\n");
        sleepWait(2);
    }
    
    public void searchSite(String searchStr) {
        //By searchTextBoxLocator = By.className("field-keywords");	
    	By searchTextBoxLocator = By.xpath("//input[@name='field-keywords']");
    	WebElement searchTextBox = driver.findElement(searchTextBoxLocator);
        searchTextBox.sendKeys(searchStr);
        System.out.println("\"" + searchStr + "\"" + " keyed in search textbox!");
        sleepWait(2);
        // 'Go' button
        By goButton = By.xpath("//input[@class='nav-input']");
        driver.findElement(goButton).submit();
        sleepWait(2);
        System.out.println("\"Go\" or Search button pressed!\n\n");
        
    }
    
    // Wait for the WebElement to be located
    // returns true - if WebElement is located
    //         false - if not
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
