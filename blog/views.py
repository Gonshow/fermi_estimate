from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post, Comment
from django_filters import rest_framework as filters
#中置記法から前置記法へ
def infix_to_prefix(INPUTED_TEXT, buffer=[],stack=[]):
    buffer=[]
    for token in INPUTED_TEXT:
        if token == '(' or token == 'c' or token == 's' or token == 't':
            stack.append(token)
        elif token == ')':
            while len(stack) > 0:
                te = stack.pop()
                if te == '(':
                    break
                else:
                    buffer.append(te)
            if len(stack) > 0:
                if stack[-1] == 'c' or stack[-1] == 's' or stack[-1] == 't':
                    buffer.append(stack.pop())
        elif token == '*' or token == '/':
            while len(stack) > 0:
                if stack[-1] == '*' or stack[-1] == '/':
                    buffer.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '+' or token == '-':
            while len(stack) > 0:
                if stack[-1] == '*' or stack[-1] == '/' or stack[-1] == '+' or stack[-1] == '-':
                    buffer.append(stack.pop())
                else:
                    break
            stack.append(token)
        else:
            buffer.append(token)

    while len(stack) > 0:
        buffer.append(stack.pop())
    return buffer
#print(INPUTED_TEXT)
#print("".join(buffer))
#前置記法から計算結果を出力
def RPN(states,parent,children,type):
    '''
    逆ポーランド記法を計算する関数
    '''
    operator = {
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: float(x) / y)
    }
    stack = []
    #print('RPN: %s' % states)
    for index, z  in enumerate(states):
        if z not in operator.keys():
            if type==0:
                obj = Comment.objects.filter(parent=parent,sub_name=z).first()
            elif type==1:
                obj = Comment.objects.filter(post=parent,sub_name=z).first()
            stack.append(obj.value)
            continue
        y = stack.pop()
        x = stack.pop()
        stack.append(operator[z](x, y))
        #print('%s %s %s =' % (x, z, y))
    #print(stack[0])

    #obj = Comment.objects.filter(pk=comment_pk)
    return stack[0]

class PostList(generic.ListView):
    """記事一覧"""
    model = Post


class PostDetail(generic.DetailView):
    """記事詳細"""
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['result'] = 20000.0
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['comment_list'] = self.object.comment_set.filter(parent__isnull=True)
        with_formula_list = self.object.comment_set.filter(formula__isnull=False).order_by("-depth")
        if len(self.object.comment_set.filter(value__isnull=True, formula__isnull=True))==0:
            try:
                num=len(with_formula_list)
                for i in range(num):
                    for fml in with_formula_list:
                        children = self.object.comment_set.filter(parent=fml)
                        fml.value=RPN(infix_to_prefix(fml.formula),fml,children,0)
                        print(fml.value)
                        fml.save()

                self.object.value = RPN(infix_to_prefix(self.object.formula),self.object.pk,context['comment_list'],1)
                self.object.save()
            except:
                self.object.value=None
                self.object.save()
        else:
            self.object.value=None
            self.object.save()
        #postがvalueを持っていればhtmlに渡して出力
        if self.object.value:
            context['result']=self.object.value
        return context
class PostCreate(generic.CreateView):
    model = Post
    fields=["title"]
class PostDelete(generic.DeleteView):
    model = Post
    success_url = "/"

# コメント、返信フォーム
CommentForm = forms.modelform_factory(Comment, fields=('text', ))
class PostUpdate(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Post

        # specify fields to be used
        fields = [ "formula"]
class UpdateForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Comment

        # specify fields to be used
        fields = [ "formula"]
class UpdateFormNum(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Comment

        # specify fields to be used
        fields = [ "value"]
def comment_create(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.depth = 1
        comment.save()
        return redirect('blog:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog/comment_form.html', context)

def post_update(request, post_pk):
    obj = get_object_or_404(Post, pk=post_pk)
    form = UpdateForm(request.POST or None, instance = obj)
    context = {
        'form': form,
    }
    context['children'] = Comment.objects.all().filter(post=obj.id, parent__isnull=True)
    dictionary = []
    d=dict()
    for child in context['children']:
        obj_child = get_object_or_404(Comment, post=post_pk,text=child)
        obj_child.sub_name = chr(ord('a')+len(dictionary))
        obj_child.save()
        dictionary.append([chr(ord('a')+len(dictionary))+":",child])
        d[chr(ord('a')+len(d))]=child
    context['dict']=dictionary
    if request.method == 'POST':
        form.save()
        fmla = list(str(obj.formula))
        fmla_out=""
        for i in fmla:
            try:
                if d[i]:
                    fmla_out=fmla_out+str(d[i])
            except:
                fmla_out=fmla_out+i
        obj.formula_out = fmla_out
        obj.save()
        """計算実行"""
        """
        with_value_list = Comment.objects.all().filter(post=post_pk,value__isnull=False)
        for l in with_value_list:
            parent_list = Comment.objects.all().filter(post=post_pk,pk=l)
        """
        return redirect('blog:post_detail', pk=obj.pk)
    return render(request, 'blog/formula_update_form.html', context)


def comment_update(request, post_pk, comment_pk):
    obj = get_object_or_404(Comment, pk=comment_pk)
    form = UpdateForm(request.POST or None, instance = obj)
    context = {
        'form': form,
    }
    context['children'] = Comment.objects.all().filter(parent=comment_pk)
    dictionary = []
    d=dict()
    for child in context['children']:
        obj_child = get_object_or_404(Comment, post=post_pk,text=child)
        obj_child.sub_name = chr(ord('a')+len(dictionary))
        obj_child.save()
        dictionary.append([chr(ord('a')+len(dictionary))+":",child])
        d[chr(ord('a')+len(d))]=child
    context['dict']=dictionary
    if request.method == 'POST':
        form.save()
        fmla = list(str(obj.formula))
        fmla_out=""
        for i in fmla:
            try:
                if d[i]:
                    fmla_out=fmla_out+str(d[i])
            except:
                fmla_out=fmla_out+i
        obj.formula_out = fmla_out
        obj.save()
        return redirect('blog:post_detail', pk=obj.post.pk)
    return render(request, 'blog/formula_update_form.html', context)




def comment_update_num(request, post_pk, comment_pk):
    obj = get_object_or_404(Comment, pk=comment_pk)
    form = UpdateFormNum(request.POST or None, instance = obj)

    if request.method == 'POST':
        form.save()
        return redirect('blog:post_detail', pk=obj.post.pk)

    context = {
        'form': form
    }
    return render(request, 'blog/num_update_form.html', context)
def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.depth = reply.parent.depth + 1
        reply.save()
        return redirect('blog:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'blog/comment_form.html', context)
