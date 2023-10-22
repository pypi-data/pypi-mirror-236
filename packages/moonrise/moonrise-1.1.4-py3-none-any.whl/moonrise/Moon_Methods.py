from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class MoonMethods:
    """Common-use methods when locating and interacting with web elements
    """

    def get_web_element(self, locator, timeout=None, get_multiples = False):
        """Locate a web element or elements via a given ``locator``.
           Throws a TimeoutException if the element(s) cannot be found within ``timeout`` or default_timeout

           Can perform a search in 3 main ways:
           - XPATH default: using the prefix '//' will automatically use XPATH to perform the search
           - CSS default: simply inputting an element locator will try to locate the element via CSS selector
           - By methods: specifying the lookup type will use the desired lookup method if it is available. Available methods include:
             - name:some_name
             - id:some_id
             - link:link_text
             - partial link text:partial_link_text
             - class:class_of_element
             - tag:element_tag
             - css:css_selector

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
           - ``get_multiples``: If get_web_element should return a list of elements that match the given locator. False by default.
        """

        # Timeout for element to be found may come from the timeout given to this method or the default_timeout.
        if timeout:
            self.wait._timeout = timeout
        else:
            self.wait._timeout = self.default_timeout

        location_methods = {
            "name": By.NAME,
            "id": By.ID,
            "link": By.LINK_TEXT,
            "xpath": By.XPATH,
            "partial link text": By.PARTIAL_LINK_TEXT,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
        }

        multi_element_return = {
            False: EC.visibility_of_element_located,
            True: EC.visibility_of_all_elements_located
        }

        try:
            if type(locator) is WebElement or type(locator) is MoonElement:
                results = locator
            elif locator.startswith("/"):
                results = self.wait.until(multi_element_return.get(get_multiples)((By.XPATH, locator)))
            elif locator.split(":")[0] in location_methods:
                results = self.wait.until(multi_element_return.get(get_multiples)((location_methods[locator.split(":")[0]], locator.split(":")[1])))
            else:
                results = self.wait.until(multi_element_return.get(get_multiples)((By.CSS_SELECTOR, locator)))
        except TimeoutException:
            raise TimeoutException(f"Could not find '{locator}' after {self.wait._timeout} seconds.")
        
        # Convert WebElement(s) to MoonElement(s)
        if type(results) is list:
            elements = []
            for e in results:
                elements.append(MoonElement(e))
            return elements
        else:
            return MoonElement(results)

    def click_element(self, locator, timeout=None):
        """Click the element identified by ``locator``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        self.get_web_element(locator=locator, timeout=timeout).click()


    def input_text(self, locator, text, timeout=None):
        """Types the given ``text`` into the text field identified by ``locator``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        self.get_web_element(locator=locator, timeout=timeout).send_keys(text)

    def get_web_elements(self, locator, timeout=None):
        """Returns a list of WebElement objects matching the ``locator``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        return self.get_web_element(locator=locator, timeout=timeout, get_multiples=True)

    def select_from_list_by_value(self, locator, value, timeout=None):
        """Select option from selection list ``locator`` by ``value``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``value``: The value to select from the list.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        Select(self.get_web_element(locator=locator, timeout=timeout)).select_by_value(value)
        
    def select_from_list_by_label(self, locator, label, timeout=None):
        """Select option from selection list ``locator`` by ``label``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``label``: The label to select from the list.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        Select(self.get_web_element(locator=locator, timeout=timeout)).select_by_visible_text(label)

    def select_from_list_by_index(self, locator, index, timeout=None):
        """Select option from selection list ``locator`` by ``index``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``index``: The index to select from the list.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        Select(self.get_web_element(locator=locator, timeout=timeout)).select_by_index(index) 

    def get_text(self, locator, timeout=None):
        """Returns the text value of the element identified by ``locator``.

           Arguments:
           - ``locator``: The method by which to locate a web element.
           - ``timeout``: How long to search for the element before throwing a TimeoutException.
        """
        return self.get_web_element(locator=locator, timeout=timeout).text
    
    def drag_element_to_element(self, dragged_locator: str, target_locator: str, timeout: int = None):
        """Clicks and drags one element to another element.

           Arguments:
           - ``dragged_locator`` (str): Locator for the element to be clicked and dragged.
           - ``target_locator`` (str): Locator for the element that the dragged element will be dragged to.
           - ``timeout`` (int, optional): Maximum time (in seconds) to search for both the dragged and target elements before throwing a TimeoutException.
        """
        dragged_element = self.get_web_element(locator=dragged_locator, timeout=timeout)
        target_element = self.get_web_element(locator=target_locator, timeout=timeout)

        ActionChains(self.moon_driver).drag_and_drop(dragged_element, target_element).perform()

    def drag_element_to_offset(self, dragged_locator: str, x_offset: int, y_offset: int, timeout: int = None):
        """Clicks and drags one element to another element.

           Arguments:
           - ``dragged_locator`` (str): Locator for the element to be clicked and dragged.
           - ``x_offset`` (int): The number of pixels to drag the element along the x axis.
           - ``y_offset`` (int): The number of pixels to drag the element along the y axis.
           - ``timeout`` (int, optional): Maximum time (in seconds) to search for the dragged element before throwing a TimeoutException.
        """
        dragged_element = self.get_web_element(locator=dragged_locator, timeout=timeout)

        ActionChains(self.moon_driver).drag_and_drop_by_offset(dragged_element, xoffset=x_offset, yoffset=y_offset).perform()

    def scroll_to_element(self, locator: str, timeout: int = None):
        """Scrolls an element into view.

           Arguments:
           - ``locator`` (str): Locator for the element to be scrolled into view.
           - ``timeout`` (int, optional): Maximum time (in seconds) to search for the element before throwing a TimeoutException.
        """
        element = self.get_web_element(locator=locator, timeout=timeout)

        self.moon_driver.execute_script("arguments[0].scrollIntoView();", element)

class MoonElement(WebElement):
    """Replacement object for standard WebElements.
       Inherits all attributes and methods of Selenium WebElements with additional methods. 
    """

    def __init__(self, element: WebElement):
        self.element = element
        self.driver = element.parent
        super().__init__(self.driver, element.id)

    def get_parent(self):
        """Return the parent element of a WebElement.
        """
        return MoonElement(self.driver.execute_script("return arguments[0].parentNode", self.element))
    
    def get_children(self, locator: str = "*"):
        """Returns all child elements of a WebElement.
           Arguments:
           - ``locator``: The method by which to locate children of the given WebElement.
        """
        elements = []
        for e in self.driver.execute_script(f"return arguments[0].querySelectorAll('{locator}')", self.element):
            elements.append(MoonElement(e))
        return elements