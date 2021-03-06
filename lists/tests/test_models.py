from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        item.save()
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='bla', list=list1)
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise

    def test_list_ordering(self):
        list_ = List.objects.create()
        item_list = [Item.objects.create(text=f'item{i}', list=list_)
                     for i in range(3)]
        self.assertEqual(list(Item.objects.all()), item_list)

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_lists_can_have_owners(self):
        user = User.objects.create(email='wrong@owner.com')
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first')
        Item.objects.create(list=list_, text='second')
        self.assertEqual(list_.name, 'first')
