from django.forms import ModelForm
from questions.models import Question, Answer, Comment


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','body', 'user']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(QuestionForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledQuestionForm(QuestionForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['body']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledQuestionForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledQuestionForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class ModifyQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['body', 'user']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['user','qualifications', 'answer_text']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(AnswerForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledAnswerForm(AnswerForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['answer_text']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledAnswerForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledAnswerForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user','body']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(CommentForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledCommentForm(CommentForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['body']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledCommentForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledCommentForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data
