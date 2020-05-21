from model.group_new_contact import New_contact


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def open_home_page(self):
        wd = self.app.wd
        if not (wd.current_url == "http://localhost/addressbook/" and len(wd.find_elements_by_name("add")) > 0):
            wd.find_element_by_link_text("home").click()

    def add_new_contact(self, new_contact):
        wd = self.app.wd
        self.open_home_page()
        wd.find_element_by_link_text("add new").click()
        self.fill_contact_form(new_contact)
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.open_home_page()
        self.contact_cache = None

    def fill_new_form_for_add_new_contact(self, new_contact):
        wd = self.app.wd
        self.fill_contact_form(new_contact)

    def delete_contact(self):
        wd = self.app.wd
        self.select_contact()
        # delete contact
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        # submit delete contact
        wd.switch_to_alert().accept()
        self.open_home_page()
        self.contact_cache = None

    def select_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def modify_contact(self, new_contact):
        wd = self.app.wd
        self.open_home_page()
        self.select_contact()
        # click button for edit contact
        wd.find_element_by_xpath("(//img[@alt='Edit'])").click()
        # fill contact form
        self.fill_contact_form(new_contact)
        # submit modification
        wd.find_element_by_name("update").click()
        wd.find_element_by_link_text("home page").click()
        self.contact_cache = None

    def fill_contact_form(self, new_contact):
        wd = self.app.wd
        self.change_field_contact("firstname", new_contact.firstname)
        self.change_field_contact("middlename", new_contact.middlename)
        self.change_field_contact("lastname", new_contact.lastname)
        self.change_field_contact("nickname", new_contact.nickname)
        self.change_field_contact("title", new_contact.title)
        self.change_field_contact("company", new_contact.company)
        self.change_field_contact("address", new_contact.address)
        self.change_field_contact("home", new_contact.home)
        self.change_field_contact("mobile", new_contact.mobile)
        self.change_field_contact("work", new_contact.work)
        self.change_field_contact("fax", new_contact.fax)
        self.change_field_contact("email", new_contact.email)
        self.change_field_contact("address2", new_contact.address2)
        self.change_field_contact("phone2", new_contact.phone2)
        self.change_field_contact("notes", new_contact.notes)

    def change_field_contact(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def count(self):
        wd = self.app.wd
        self.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.open_home_page()
            contacts = wd.find_elements_by_name("entry")
            self.contact_cache = []
            for element in contacts:
                fname = element.find_element_by_css_selector("td:nth-child(3)").text
                lname = element.find_element_by_css_selector("td:nth-child(2)").text
                id = element.find_element_by_name("selected[]").get_attribute("value")
                self.contact_cache.append(
                     New_contact(firstname=fname, lastname=lname, id=id))
        return list(self.contact_cache)
