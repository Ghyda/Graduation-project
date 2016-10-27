from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone, datetime
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from questions.forms import QuestionForm, DisabledQuestionForm, AnswerForm, DisabledAnswerForm, CommentForm, DisabledCommentForm

from .models import Answer, Question, Comment, Vote


class IndexView(generic.ListView):
    template_name = 'questions/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'questions/detail.html'

    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'questions/detail.html', {'question': question})


class AnswersView(generic.DetailView):
    model = Question
    template_name = 'questions/answers.html'

    def answers(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'questions/answers.html', {'question': question})


class VoteView(generic.DetailView):
    model = Vote
    template_name = 'questions/vote.html'

    def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_answer = question.answer_set.get(pk=request.POST['answer'])
        except (KeyError, Answer.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'questions/detail.html', {
                'question': question,
                'error_message': "You didn't post an answer.",
            })
        else:
            selected_answer.votes += 1
            selected_answer.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('questions:answers', args=(question.id,)))


#cheat part:

@login_required
@permission_required('questions.add_question', raise_exception=True)
def create_question(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        form = QuestionForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('questions:list'))
        else:
            context = {'form': form}
            return render(request, 'questions/new.html', context)
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'questions/new.html', context)


@login_required
def edit_question(request, question_id):
    existing_question = get_object_or_404(Question, pk=question_id)

    if not request.user == existing_question.user and \
       not request.user.has_perm('questions.change_question'):
        raise PermissionDenied

    if request.method == 'POST':
        if request.user == existing_question.user:
            modified_question = DisabledQuestionForm(request.POST, instance=existing_question)
        else:
            modified_question = QuestionForm(request.POST, instance=existing_question)
        modified_question.save()
        return HttpResponseRedirect(reverse('questions:show',
                                            args=(question_id,)))
    else:
        existing_question = get_object_or_404(Question, pk=question_id)
        if request.user == existing_question.user:
            form = DisabledQuestionForm(instance=existing_question)
        else:
            form = QuestionForm(instance=existing_question)
        context = {'form': form, 'question_id': question_id}
        return render(request, 'questions/edit.html', context)

@login_required
@permission_required('questions.add_answer', raise_exception=True)
def create_answer(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        form = AnswerForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('answers:list'))
        else:
            context = {'form': form}
            return render(request, 'answers/new.html', context)
    else:
        form = AnswerForm()
        context = {'form': form}
        return render(request, 'answers/new.html', context)


@login_required
def edit_answer(request, answer_id):
    existing_answer = get_object_or_404(Answer, pk=answer_id)

    if not request.user == existing_answer.user and \
       not request.user.has_perm('answers.change_answer'):
        raise PermissionDenied

    if request.method == 'POST':
        if request.user == existing_answer.user:
            modified_answer = DisabledAnswerForm(request.POST, instance=existing_answer)
        else:
            modified_answer = AnswerForm(request.POST, instance=existing_answer)
        modified_answer.save()
        return HttpResponseRedirect(reverse('answers:show',
                                            args=(answer_id,)))
    else:
        existing_answer = get_object_or_404(Answer, pk=answer_id)
        if request.user == existing_answer.user:
            form = DisabledAnswerForm(instance=existing_answer)
        else:
            form = AnswerForm(instance=existing_answer)
        context = {'form': form, 'answer_id': answer_id}
        return render(request, 'answers/new.html', context)

@login_required
@permission_required('answers.add_comment', raise_exception=True)
def create_comment(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        form = CommentForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('answers:list'))
        else:
            context = {'form': form}
            return render(request, 'answers/comments.html', context)
    else:
        form = CommentForm()
        context = {'form': form}
        return render(request, 'answers/comments.html', context)


@login_required
def edit_comment(request, comment_id):
    existing_comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user == existing_comment.user and \
       not request.user.has_perm('answers.change_comment'):
        raise PermissionDenied

    if request.method == 'POST':
        if request.user == existing_comment.user:
            modified_comment = DisabledCommentForm(request.POST, instance=existing_comment)
        else:
            modified_comment = CommentForm(request.POST, instance=existing_comment)
        modified_comment.save()
        return HttpResponseRedirect(reverse('comments:show',
                                            args=(comment_id,)))
    else:
        existing_comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == existing_comment.user:
            form = DisabledCommentForm(instance=existing_comment)
        else:
            form = CommentForm(instance=existing_comment)
        context = {'form': form, 'comment_id': comment_id}
        return render(request, 'answers/comments.html', context)
