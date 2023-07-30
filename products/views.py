from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic.base import ContextMixin

from .models import Category, Product, Comment, CommentLike, CommentDislike, Question, Answer, AnswerLike, AnswerDislike
from profiles.recent_visits import RecentVisits
from .forms import CommentForm, QuestionForm, AnswerForm
from .paginator import CustomPaginator


class ProductCategoryView(View):
    def get(self, request, category_name, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        if not category.sub_categories.exists():
            raise Http404()

        sub_categories = category.sub_categories.all()

        return render(request, "products/product_category.html",
                      context={"title": category_name, "sub_categories": sub_categories})


class ProductSubCategoryListView(View):
    def get(self, request, category_name, *args, **kwargs):
        if request.session.get("query_name"):
            del request.session["query_name"]
        category = get_object_or_404(Category, category_name=category_name)
        if category.sub_categories.exists():
            raise Http404()

        products = Product.objects.filter(category=category).order_by("-modified_datetime")

        paginator = CustomPaginator(products, 2)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        range_pages_product = page_obj.paginator.get_elided_page_range(number=page, on_each_side=1)

        return render(request, "products/product_sub_category_list.html",
                      context={"title": category_name, "products": products,
                               "page_obj": page_obj, "range_pages": range_pages_product})


class ProductDetailView(ContextMixin, View):
    def get_object(self):
        category = get_object_or_404(Category, category_name=self.kwargs["category_name"])
        product = get_object_or_404(Product, category=category, pk=self.kwargs["pk"])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = product.comments.order_by("-modified_datetime")
        questions = product.questions.order_by("-modified_datetime")
        context["product"] = product
        context["comments"] = comments
        context["questions"] = questions
        context["question_form"] = QuestionForm()
        context["answer_form"] = AnswerForm()

        paginator_comment = CustomPaginator(comments, 2)
        page_1 = self.request.GET.get("page1")
        page_obj_comment = paginator_comment.get_page(page_1)
        range_pages_comment = page_obj_comment.paginator.get_elided_page_range(number=page_1, on_each_side=1)
        context["page_obj_comment"] = page_obj_comment
        context["range_pages_comment"] = range_pages_comment

        paginator_comment = CustomPaginator(questions, 2)
        page_2 = self.request.GET.get("page2")
        page_obj_question = paginator_comment.get_page(page_2)
        range_pages_question = page_obj_question.paginator.get_elided_page_range(number=page_2, on_each_side=1)
        context["page_obj_question"] = page_obj_question
        context["range_pages_question"] = range_pages_question

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        recent_visits = RecentVisits(request)
        product = self.get_object()
        recent_visits.add_product(product)

        if request.user.is_authenticated:
            comment = Comment.objects.filter(user=request.user, product=product)
            comment_form = CommentForm(instance=comment.first()) if comment.exists() else CommentForm()
        else:
            comment_form = CommentForm()

        context["comment_form"] = comment_form
        return render(request, "products/product_detail.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        product = self.get_object()
        comment = Comment.objects.filter(user=request.user, product=product)
        comment_form = CommentForm(instance=comment.first())

        if "send_comment" in request.POST:
            comment_form = CommentForm(request.POST, instance=comment.first())
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.product = product
                if "is_anonymous" in request.POST:
                    new_comment.is_anonymous = True
                new_comment.save()
                messages.success(request, _("Your comment was successfully submitted."))
                return redirect("products:product_detail", kwargs["category_name"], kwargs["pk"])

        elif "send_question" in request.POST:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.product = product
                question.user = request.user
                question.save()
                messages.success(request, _("Your question was successfully submitted."))
                return redirect("products:product_detail", kwargs["category_name"], kwargs["pk"])

            context["question_form"] = question_form

        elif "send_answer" in request.POST:
            answer_form = AnswerForm(request.POST)
            question = get_object_or_404(Question, pk=int(request.POST["id_question"]))
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.product = product
                answer.user = request.user
                answer.question = question
                answer.save()
                messages.success(request, _("Your answer was successfully submitted."))
                return redirect("products:product_detail", kwargs["category_name"], kwargs["pk"])

            context["answer_form"] = answer_form

        context["comment_form"] = comment_form

        return render(request, "products/product_detail.html", context)


class ProductLikeComment(View):
    def post(self, request, id_comment, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=id_comment)
        try:
            comment_like = CommentLike.objects.get(user=request.user, comment=comment)
        except CommentLike.DoesNotExist:
            CommentLike.objects.create(user=request.user, comment=comment)
            return JsonResponse({"status": "liked"})
        else:
            comment_like.delete()
            return JsonResponse({"status": "retake_liked"})


class ProductDislikeComment(View):
    def post(self, request, id_comment, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=id_comment)
        try:
            comment_dislike = CommentDislike.objects.get(user=request.user, comment=comment)
        except CommentDislike.DoesNotExist:
            CommentDislike.objects.create(user=request.user, comment=comment)
            return JsonResponse({"status": "disliked"})
        else:
            comment_dislike.delete()
            return JsonResponse({"status": "retake_disliked"})


class ProductLikeAnswer(View):
    def post(self, request, id_answer, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=id_answer)
        try:
            answer_like = AnswerLike.objects.get(user=request.user, answer=answer)
        except AnswerLike.DoesNotExist:
            AnswerLike.objects.create(user=request.user, answer=answer)
            return JsonResponse({"status": "liked"})
        else:
            answer_like.delete()
            return JsonResponse({"status": "retake_liked"})


class ProductDislikeAnswer(View):
    def post(self, request, id_answer, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=id_answer)
        try:
            answer_dislike = AnswerDislike.objects.get(user=request.user, answer=answer)
        except AnswerDislike.DoesNotExist:
            AnswerDislike.objects.create(user=request.user, answer=answer)
            return JsonResponse({"status": "disliked"})
        else:
            answer_dislike.delete()
            return JsonResponse({"status": "retake_disliked"})
