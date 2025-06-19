from .base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.profile_name_input = page.locator("#name")
        self.save_changes_button = page.get_by_role("button", name="Save changes")
        self.profile_success_update_popup = page.get_by_text("Profile successfully updated")

        self.category_name_input = page.get_by_placeholder("Add new category")
        self.archive_dialog = page.get_by_role("dialog")
        self.archive_dialog_button = self.archive_dialog.get_by_role("button", name="Archive")
        self.is_archive_include_checkbox = page.get_by_label("Show archived")
        self.edit_category_input = page.get_by_placeholder("Edit category")
        self.category_succes_edit_popup = page.get_by_text(f"Category name is changed")


    def change_profile_name(self, profile_name: str):
        self.profile_name_input.fill(profile_name)
        self.save_changes_button.click()
        self.profile_success_update_popup.wait_for()
    
    def add_category(self, category_name: str):
        self.category_name_input.fill(category_name)
        self.category_name_input.press("Enter")
        self.page.get_by_text(f"You've added new category: {category_name}").wait_for()

    def archive_category(self, category_name: str):
        category = self.page.locator("div.MuiBox-root", has=self.page.locator("span", has_text=category_name))
        category.locator('button[aria-label="Archive category"]').click()
        self.archive_dialog.wait_for()
        self.archive_dialog_button.click()
        self.page.get_by_text(f"Category {category_name} is archived").wait_for()
    
    def edit_category(self, category_name: str, new_category_name: str):
        category = self.page.locator("div.MuiBox-root", has=self.page.locator("span", has_text=category_name))
        category.locator('button[aria-label="Edit category"]').click()
        self.edit_category_input.click()
        self.edit_category_input.fill(new_category_name)
        self.edit_category_input.press("Enter")
        self.category_succes_edit_popup.wait_for()


        
        