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

class Question:
    def __init__(self,**kwargs):
        self.__kind = kwargs.pop("kind", None)
        self.__question = kwargs.pop("question", None)
        self.__tags = kwargs.pop("tags", None)
        self.__answer = kwargs.pop("answer", None)
        self.__uuid = kwargs.pop("uuid", None)
        self.__additional_args = kwargs

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
    def answer(self):
        return self.__answer
    @property
    def uuid(self):
        return self.__uuid
    @property
    def args(self):
        return self.__additional_args


class TFQuestion(ipw.VBox):
    def __init__(self, questions):
        self.questions = questions
        self.qlabel = ipw.Label(value="Enter question using Markdown formatting")
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
        
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"TF"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            q["correct_answer"] = self.answer.value
            q["feedback"] = {"T":self.tfb.value, "F":self.ffb.value}
            q["uuid"] = uuid.uuid1()
            self.questions.append(q)

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
        
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"MC"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            q["correct_answer"] = self.answer.value
            tmp = {}
            for i in range(self.num_answers):
                tmp[i] = {"answer": self.answers[i].value,
                          "feedback": self.feedback[i].value}
            q["answers"] = tmp
            q["uuid"] = uuid.uuid1()

            self.questions.append(q)
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
        
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"AT"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value

            tmp = {}
            for i in range(self.num_answers):
                tmp[i] = {"answer": self.answers[i].value,
                          "feedback": self.feedback[i].value,
                          "status": self.status[i].value}
            q["answers"] = tmp
            q["uuid"] = uuid.uuid1()

            self.questions.append(q)
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
        
        
    def commit_question(self, *args):
        try:
            self.qlabel.value = "submitted"
            q = {"kind":"FR"}
            q["question"] = self.question.value
            q["tags"] = self.tags.value
            q["feedback"] = self.feedback.value
            q["uuid"] = uuid.uuid1()

            self.questions.append(q)
        except Exception as error:
            self.qlabel.value = "submission failed: %s"%error            

class QWidget(ipw.VBox):
    def __init__(self, q):
        self.__q = q
        super(QWidget, self).__init__(q)


    def kind(self):
        return self.__q["kind"]
    def question(self):
        return self.__q["question"]
    def tags(self):
        return self.__q["tags"]
    def feedback(self):
        return self.__q["feedback"]
class FRWidget(ipw.VBox):
    def __init__(self, q):
        if q["kind"] != "FR":
            raise TypeError("wrong type of question")
        self.__q = q
        self.label = ipw.Label(value="Free Response")
        self.description = ipw.HTML(markdown.markdown(q["question"]))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit")
        self.answer = ipw.Textarea(value="", placeholder="Type answer here.")
        self.submit.on_click(self.onsubmit)
        super(FRWidget, self).__init__(children=[self.description, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
    def onsubmit(self, *args):
        try:
            self.feedback.value = markdown.markdown(self.__q["feedback"])
        except Exception as error:
            self.label.value = error


class TFWidget(ipw.VBox):
    def __init__(self, q):
        if q["kind"] != "TF":
            raise TypeError("wrong type of question")
        self.__q = q
        self.label = ipw.Label(value="Question")
        self.description = ipw.HTML(markdown.markdown(q["question"]))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit")
        self.answer = ipw.RadioButtons( options = ["T","F"],
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(TFWidget, self).__init__(children=[self.label,
                                                 self.description, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
    def onsubmit(self, *args):
        try:
            template = "%s %s"
            if self.answer.value == self.__q["correct_answer"]:
                mode = "Correct: "
            else:
                mode = "Incorrect: "
            self.feedback.value = template%(mode,
                                            markdown.markdown(self.__q["feedback"][self.answer.value]))
        except Exception as error:
            self.label.value = error

class MCWidget(ipw.VBox):
    def __init__(self, q):
        if q["kind"] != "MC":
            raise TypeError("wrong type of question")
        self.__q = q
        self.label = ipw.Label(value="Select the Correct Answer")
        self.question = ipw.HTML(markdown.markdown(q["question"]))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit") 
        self.__sanswers = list(q["answers"].items())
        random.shuffle(self.__sanswers)
        options = [a[1]["answer"] for a in self.__sanswers]
        self.answer = ipw.RadioButtons( options = options,
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(MCWidget, self).__init__(children=[self.label,
                                                 self.question, 
                                                 self.answer, 
                                                 self.submit,
                                                 self.feedback])
    def iscorrect(self, a):
        return self.__q["answers"][self.__q["correct_answer"]]["answer"] == a
        

    def aindex(self, a):
        return [_a[1]["answer"] for _a in self.__sanswers].index(a)
            
    def onsubmit(self, *args):
        try:
            template = "<h3>%s</h3> %s"
            if self.iscorrect(self.answer.value):
                mode = "Correct: "
            else:
                mode = "Incorrect: "
            self.feedback.value = template%(mode,
                                            markdown.markdown(self.__sanswers[self.aindex(self.answer.value)][1]["feedback"]))
        except Exception as error:
            self.label.value = "error in onsubmit: %s %s"%(self.answer.value, str(error))

class ATWidget(ipw.VBox):
    def __init__(self, q):
        if q["kind"] != "AT":
            raise TypeError("wrong type of question")
        self.__q = q
        self.label = ipw.Label(value="Select all True Answers")
        self.question = ipw.HTML(markdown.markdown(q["question"]))
        self.feedback = ipw.HTML()
        self.submit = ipw.Button(description="submit") 
        self.__sanswers = list(q["answers"].items())
        random.shuffle(self.__sanswers)
        options = [a[1]["answer"] for a in self.__sanswers]
        self.answer = ipw.SelectMultiple( options = options,
                                            description = '')
        self.submit.on_click(self.onsubmit)
        super(ATWidget, self).__init__(children=[self.label,
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
                if a[1]["answer"] in self.answer.value:
                    if self.istrue(a[1]["answer"]):
                        mode = "Correct: "
                    else:
                        mode = "Incorrect: "
                else:
                    if self.istrue(a[1]["answer"]):
                        mode = "Incorrect: "
                    else:
                        mode = "Correct: "
                fb = fb + "<h4>%s %s</h4> %s\n"%(mode,
                                                 a[1]["answer"],
                                                       markdown.markdown(a[1]["feedback"]))
                    

            self.feedback.value = fb
        except Exception as error:
            self.label.value = "error in onsubmit: %s %s"%(self.answer.value, str(error))

def get_widget(q):
    if q["kind"] == "TF":
        return TFWidget(q)
    elif q["kind"] == "MC":
        return MCWidget(q)
    elif q["kind"] == "AT":
        return ATWidget(q)
    elif q["kind"] == "FR":
        return FRWidget(q)
    else:
        raise ValueError("no matching widget for question type")

def save_questions(questions, file):
    with open(os.path.join(dminteract.DBDIR, file), "w") as fp:
        yaml.dump_all(questions,fp)


def load_questions(file):
    """

    """
    with open(os.path.join(dminteract.DBDIR, file), "r") as fp:
        questions = list(yaml.load_all(fp, Loader=yaml.SafeLoader))
    return questions
