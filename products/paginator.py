from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def get_elided_page_range(self, number=1, on_each_side=3, *args):
        page_obj = self.get_page(number)
        last_page_number = self.num_pages
        before_and_after_page_count = on_each_side
        list_show_pages = [1, self.num_pages]

        if last_page_number - (2 * before_and_after_page_count) > 2 * before_and_after_page_count:
            if page_obj.number == 1:
                list_show_pages[1:1] = [2, 3]
            elif page_obj.number == last_page_number:
                list_show_pages[-1:-1] = [last_page_number - 2, last_page_number - 1]
            else:
                list_between_pages = []
                for index in range(-before_and_after_page_count, before_and_after_page_count + 1):
                    if page_obj.number + index not in list_show_pages:
                        list_between_pages.append(page_obj.number + index)
                list_show_pages[1:1] = list_between_pages
        else:
            list_show_pages = self.page_range

        flag = False
        for num in self.page_range:
            if num in list_show_pages:
                flag = False
                yield num
            elif num not in list_show_pages and flag is False:
                yield self.ELLIPSIS
                flag = True
