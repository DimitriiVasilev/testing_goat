from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        window_size = self.browser.get_window_size()

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            window_size['width'] / 2 - inputbox.size['width'] / 2,
            inputbox.location['x'],
            delta=5
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            window_size['width'] / 2 - inputbox.size['width'] / 2,
            inputbox.location['x'],
            delta=5
        )
