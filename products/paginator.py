from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def get_elided_page_range(self, number=1, on_each_side=3, *args):
        page_obj = self.get_page(number)
        LAST_PAGE_NUMBER = self.num_pages
        BEFORE_AND_AFTER_PAGE_COUNT = on_each_side
        list_show_pages = [1, self.num_pages]

        if LAST_PAGE_NUMBER - (2 * BEFORE_AND_AFTER_PAGE_COUNT) > 2 * BEFORE_AND_AFTER_PAGE_COUNT:
            if page_obj.number == 1:
                list_show_pages[1:1] = [2, 3]
            elif page_obj.number == LAST_PAGE_NUMBER:
                list_show_pages[-1:-1] = [LAST_PAGE_NUMBER - 2, LAST_PAGE_NUMBER - 1]
            else:
                list_between_pages = []
                for index in range(-BEFORE_AND_AFTER_PAGE_COUNT, BEFORE_AND_AFTER_PAGE_COUNT + 1):
                    if page_obj.number + index not in list_show_pages:
                        list_between_pages.append(page_obj.number + index)
                list_show_pages[1:1] = list_between_pages
        else:
            list_show_pages = self.page_range

        for num in self.page_range:
            if num in list_show_pages:
                yield num
            else:
                yield self.ELLIPSIS
