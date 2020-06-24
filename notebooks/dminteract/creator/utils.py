"""
utils for creating, displaying, and saving question/answers


"""
import uuid
import random
import os

import ipywidgets as ipw
import markdown
import random
import yaml
import tempfile
import pickle

from .. __init__ import _dbdir, _datadir
TEMPDIR = tempfile.gettempdir()

def save_temp_questions(qs):
    with open(os.path.join(TEMPDIR, "questions.pickle"), "wb") as fp:
        pickle.dump(qs, fp)

class Question:
    def __init__(self,**kwargs):
        self.__kind = kwargs.pop("kind", None)
        self.__question = kwargs.pop("question", None)
        self.__tags = kwargs.pop("tags", None)
        self.__responses = kwargs.pop("responses", None)
        self.__uuid = kwargs.pop("uuid", None)
        self.__additional_args = kwargs
    def to_dict(self):
        return {"kind":self.kind, "question":self.question,
                "tags":self.tags, "responses":self.responses,
                "uuid":self.uuid}

    @property
    def kind(self):
        return self.__kind
    @property
    def question(self):
        return self.__question
    @property
    def tags(self):
        return self.__tags
    @property
    def responses(self):
        return self.__responses
    @property
    def uuid(self):
        return self.__uuid
    @property
    def args(self):
        return self.__additional_args


class TFQuestion(ipw.VBox):
    prompt = "Enter question using Markdown formatting"
    def __init__(self, questions):
        self.questions = questions
        self.qlabel = ipw.Label(value=self.prompt)
        self.question = ipw.Textarea()
        self.tags = ipw.Text(description="tags")
        self.qtbox = ipw.VBox([self.qlabel, self.question, self.tags])
        self.answer = ipw.RadioButtons(options=['T', 'F'])
        self.qbox = ipw.HBox([self.qtbox, self.answer])
        self.tfb = ipw.Textarea(description = "True Feedback")
        self.ffb = ipw.Textarea(description="False Feedback")
        self.feedback = ipw.Tab()
        self.feedback.children = [self.tfb, self.ffb]
        self.commit = ipw.Button(description="commit")
        self.commit.on_click(self.commit_question)
        super(TFQuestion, self).__init__(children=[self.qbox, self.feedback, self.commit])
        
    def reset_question(self):
        self.question.value = ""
        self.tfb.value = ""
        self.ffb.value = ""
    def commit_question(self, *args):
        try:
            q = {"kind":"TF"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            tmp = {}
            responses = ['T','F']
            for i in range(2):
                tmp[responses[i]] = {
                          "status":responses[i] == self.answer.value,
                          "feedback": self.tfb.value if responses[i] == 'T' else self.ffb.value}
            q["responses"] = tmp
            q["uuid"] = str(uuid.uuid1())
            self.questions.append(Question(**q))
            self.reset_question()
            save_temp_questions(self.questions)

        except Exception as error:
            self.qlabel.value = "submission failed: %s"%error
                
        
   
class MCQuestion(ipw.VBox):
    def __init__(self, questions, num_answers = 4):
        self.questions = questions
        self.num_answers = num_answers
        self.qlabel = ipw.Label(value="Enter question using Markdown formatting")
        self.question = ipw.Textarea()
        self.tags = ipw.Text(description="tags")
        self.qtbox = ipw.VBox([self.qlabel, self.question, self.tags]) 
        self.answers = [ipw.Textarea(description="Ans %d"%i) for i in range(num_answers)]
        self.feedback = [ipw.Textarea(description="Feedback %d"%i) for i in range(num_answers)]
        self.atab = ipw.Tab()
        self.answer = ipw.Dropdown(options=list(range(num_answers)), value=0,
                                   description="Correct Answer")
        self.atab.children = [ipw.HBox(list(a)) for a in zip(self.answers,self.feedback)]
        self.abox = ipw.VBox([self.answer, self.atab])

        self.commit = ipw.Button(description="commit")
        self.commit.on_click(self.commit_question)
        super(MCQuestion, self).__init__(children=[self.qtbox, self.abox, self.commit])
        
    
    def reset_question(self):
        self.question.value = ""
        for a in self.answers:
            a.value = ""
        for a in self.feedback:
            a.value = ""

    def commit_question(self, *args):
        try:
            q = {"kind":"MC"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            tmp = {}
            for i in range(self.num_answers):
                tmp[self.answers[i].value] = {
                          "status": i==self.answer.value,
                          "feedback": self.feedback[i].value}
            q["responses"] = tmp
            q["uuid"] = str(uuid.uuid1())

            self.questions.append(Question(**q))
            self.reset_question()
            save_temp_questions(self.questions)
        except Exception as error:
            self.qlabel.value = "submission failed: %s"%error


class ATQuestion(ipw.VBox):
    def __init__(self, questions, num_answers = 4):
        self.questions = questions
        self.num_answers = num_answers
        self.qlabel = ipw.Label(value="Enter question using Markdown formatting")
        self.question = ipw.Textarea()
        self.tags = ipw.Text(description="tags")
        self.qtbox = ipw.VBox([self.qlabel, self.question, self.tags]) 
        self.answers = [ipw.Textarea(description="Ans %d"%i) for i in range(num_answers)]
        self.feedback = [ipw.Textarea(description="Feedback %d"%i) for i in range(num_answers)]
        self.status = [ipw.RadioButtons(options=["T", "F"]) for i in range(num_answers)]
        self.atab = ipw.Tab()

        self.atab.children = [ipw.HBox(list(a)) for a in zip(self.answers,
                                                                        self.feedback,
                                                                        self.status)]

        self.commit = ipw.Button(description="commit")
        self.commit.on_click(self.commit_question)
        super(ATQuestion, self).__init__(children=[self.qtbox, self.atab, self.commit])
        
    def reset_question(self):
        self.question.value = ""
        for a in self.answers:
            a.value = ""
        for a in self.feedback:
            a.value = ""
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"AT"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            tmp = {}
            for i in range(self.num_answers):
                tmp[self.answers[i].value] = {
                          "feedback": self.feedback[i].value,
                          "status": self.status[i].value=='T'}
            q["responses"] = tmp
            q["uuid"] = str(uuid.uuid1())

            self.questions.append(Question(**q))
            self.reset_question()
            save_temp_questions(self.questions)
        except Exception as error:
            self.qlabel.value = "submission failed: %s"%error

class FRQuestion(ipw.VBox):
    def __init__(self, questions):
        self.questions = questions
        self.qlabel = ipw.Label(value="Enter question using Markdown formatting")
        self.question = ipw.Textarea()
        self.tags = ipw.Text(description="tags")
        self.qtbox = ipw.VBox([self.qlabel, self.question, self.tags]) 

        self.feedback = ipw.Textarea(description="Feedback")


        self.commit = ipw.Button(description="commit")
        self.commit.on_click(self.commit_question)
        super(FRQuestion, self).__init__(children=[self.qtbox, self.feedback, self.commit])
        
    def reset_question(self):
        self.question.value = ""
        self.feedback.value = ""
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"FR"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value
            q["responses"] = {0:{"status":None, "feedback":self.feedback.value}}
            q["uuid"] = str(uuid.uuid1())

            self.questions.append(Question(**q))
            self.reset_question()
            save_temp_questions(self.questions)
        except Exception as error:
            self.qlabel.value = "submission failed: %s"%error            


class QWidget(ipw.VBox):
    def __init__(self, q, *args, **kwargs):
        self.__q = q
        super(QWidget,self).__init__(*args, **kwargs)

    @property
    def q(self):
        return self.__q

class FRWidget(QWidget):
    def __init__(self, q):
        if q.kind != "FR":
            raise TypeError("wrong type of question")
        self.label = ipw.Label(value="Free Response")
        self.description = ipw.HTML(markdown.markdown(q.question))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit")
        self.answer = ipw.Textarea(value="", placeholder="Type answer here.")
        self.submit.on_click(self.onsubmit)
        super(FRWidget, self).__init__(q, children=[self.description, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
    def onsubmit(self, *args):
        try:
            self.feedback.value = markdown.markdown(self.q.responses[0]["feedback"])
        except Exception as error:
            self.label.value = error


class TFWidget(QWidget):
    def __init__(self, q):
        if q.kind != "TF":
            raise TypeError("wrong type of question")
        self.label = ipw.Label(value="Question")
        self.description = ipw.HTML(markdown.markdown(q.question))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit")
        self.answer = ipw.RadioButtons( options = ["T","F"],
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(TFWidget, self).__init__(q, children=[self.label,
                                                 self.description, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])


    def onsubmit(self, *args):
        try:
            template = "%s %s"
            if self.q.responses[self.answer.value]["status"]:
                mode = "Correct: "
            else:
                mode = "Incorrect: "
            self.feedback.value = template%(mode,
                                            markdown.markdown(self.q.responses[self.answer.value]["feedback"]))
        except Exception as error:
            self.label.value = error

class MCWidget(QWidget):
    def __init__(self, q):
        if q.kind != "MC":
            raise TypeError("wrong type of question")
        self.label = ipw.Label(value="Select the Correct Answer")
        self.question = ipw.HTML(markdown.markdown(q.question))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit") 
        self.__sanswers = list(q.responses.items())
        random.shuffle(self.__sanswers)
        options = [a[0] for a in self.__sanswers]
        self.answer = ipw.RadioButtons( options = options,
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(MCWidget, self).__init__(q, children=[self.label,
                                                 self.question, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
            
    def onsubmit(self, *args):
        try:
            template = "<h3>%s</h3> %s"
            ind = [a[0] for a in self.__sanswers].index(self.answer.value)
            if self.__sanswers[ind][1]["status"]:
                mode = "Correct: "
            else:
                mode = "Incorrect: "
            self.feedback.value = template%(mode,
                                            markdown.markdown(self.__sanswers[ind][1]["feedback"]))
        except Exception as error:
            self.label.value = "error in onsubmit: %s %s"%(self.answer.value, str(error))

class ATWidget(QWidget):
    def __init__(self, q):
        if q.kind != "AT":
            raise TypeError("wrong type of question")
        self.__q = q
        self.label = ipw.Label(value="Select all True Answers")
        self.question = ipw.HTML(markdown.markdown(q.question))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit") 
        self.__sanswers = list(q.responses.items())
        random.shuffle(self.__sanswers)
        options = [a[0] for a in self.__sanswers]
        self.answer = ipw.SelectMultiple( options = options,
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(ATWidget, self).__init__(q, children=[self.label,
                                                 self.question, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
    def istrue(self, a):
        index = self.aindex(a)
        return self.__sanswers[index][1]["status"] == "T"
        

    def aindex(self, a):
        return [_a[1]["answer"] for _a in self.__sanswers].index(a)
            
    def onsubmit(self, *args):
        try:
            fb = ""
            for a in self.__sanswers:
                if a[0] in self.answer.value:
                    if a[1]["status"]:
                        mode = "Correct: "
                    else:
                        mode = "Incorrect: "
                else:
                    if a[1]["status"]:
                        mode = "Incorrect: "
                    else:
                        mode = "Correct: "
                fb = fb + "<h4>%s %s</h4> %s\n"%(mode,
                                                 a[0],
                                                       markdown.markdown(a[1]["feedback"]))
                    

            self.feedback.value = fb
        except Exception as error:
            self.label.value = "error in onsubmit: %s %s"%(self.answer.value, str(error))

def get_widget(q):
    if q.kind == "TF":
        return TFWidget(q)
    elif q.kind == "MC":
        return MCWidget(q)
    elif q.kind == "AT":
        return ATWidget(q)
    elif q.kind == "FR":
        return FRWidget(q)
    else:
        raise ValueError("no matching widget for question type")

def save_questions(questions, file):
    with open(os.path.join(_dbdir(), file), "w") as fp:
        yaml.dump_all([q.to_dict() for q in questions],fp)


def load_questions(file):
    """

    """
    with open(os.path.join(_dbdir(), file), "r") as fp:
        questions = [Question(**q) for q in yaml.load_all(fp, Loader=yaml.SafeLoader)]
    return questions

def create_question_bank(qfile, tag=None):
    _questions = load_questions(qfile)
    if tag:
        return [get_widget(q) for q in _questions if tag in q.tags]
    else:
        return [get_widget(q) for q in _questions]

