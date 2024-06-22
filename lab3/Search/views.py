from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from manager.statistic import statistic
from manager.teacher import teacher
from manager.project import project
from manager.paper import paper
from manager.course import course
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re
def get_teacher_name(request):
    manager = teacher()
    job_number = request.GET.dict()['job_number']
    if job_number:
        try:
            result = manager.search_id(job_number)
            print(result)
            print(result[0]['name'])

            return JsonResponse({'success': True, 'name': result[0]['name']})
        except Exception as e:
            return JsonResponse({'success': False, 'message': '未找到该工号对应的老师'})
    return JsonResponse({'success': False, 'message': '未找到该工号对应的老师'})

def teacher_insert(request: HttpRequest):
    if request.method == 'POST':
        print(data)
        manager = teacher()
        data = request.POST.dict()
        try:
            manager.insert(data)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    return render(request, 'teacher/insert.html')

def teacher_update(request: HttpRequest):
    manager = teacher()
    job_numbers = request.path[9:13]
    if request.method == 'POST':
        data = request.POST.dict()
        data['job_numbers'] = job_numbers
        try:
            manager.update(data)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    else:
        dict = manager.search_id(job_numbers)
        return render(request, 'teacher/update.html', dict)
    
def teacher_search(request: HttpRequest):
    manager = teacher()
    if request.method == 'POST':
        job_numbers = request.POST.dict()['job_numbers']
        try:
            manager.delete(job_numbers)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')

    if 'query' in request.GET.dict():
        query = request.GET.dict()['query']
        teacher_list = []
        try:
            result = manager.search_id(query)
            teacher_list.append(result)
        except:
            pass
        try:
            results = manager.search_name(query)
            teacher_list.extend(results)
        except:
            pass
        return render(request, 'teacher/search.html', {
            'query': query,
            'num': len(teacher_list),
            'teacher_list': teacher_list
        })
    return render(request, 'teacher/search.html')

def teacher_delete(request: HttpRequest):
    manager = teacher()
    job_numbers = request.path[9:13]
    try:
        manager.delete(job_numbers)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('success')

def project_insert(request: HttpRequest):
    if request.method == 'POST':
        manager = project()
        data = request.POST.dict()
        data['project_type'] = project_type_int(data['project_type'])
        data['teacher_index_list'] = string_to_list(data['teacher_index_list'])
        
        manager.insert(data)
        subdata = data.copy()
        print(data)
        try:
            for i in data['teacher_index_list']:
                subdata['job_number'] = data['teacher_id_' + str(i)]
                subdata['own_money'] = data['teacher_budget_' + str(i)]
                subdata['ranking'] = data['teacher_position_' + str(i)]
                manager.insert_charge_project(subdata)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    return render(request, 'project/insert.html')

def project_update(request: HttpRequest):
    manager = project()
    # print(request)
    project_id = request.path[9:14]
    # print(project_id)
    if request.method == 'POST':
        data = request.POST.dict()
        data['project_number'] = project_id
        data['project_type'] = project_type_int(data['project_type'])
        data['teacher_index_list'] = string_to_list(data['teacher_index_list'])
        print(data)
        manager.delete(project_id)
        subdata = data.copy()
        
        try:
            for i in data['teacher_index_list']:
                subdata['job_number'] = data['teacher_id_' + str(i)]
                subdata['own_money'] = data['teacher_budget_' + str(i)]
                subdata['ranking'] = data['teacher_position_' + str(i)]
                manager.update_projectself(subdata)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    else:
        dict = manager.search_project_number(project_id)
        print(dict)
        dict2 = manager.search_teacher(project_id)
        print(dict2)
        return render(request, 'project/update.html', {
            'project_number': dict['project_number'],
            'project_name': dict['project_name'],
            'project_source': dict['project_source'],
            'project_type': dict['project_type'],
            'total_budget': dict['total_budget'],
            'start_year': str(dict['start_year']),
            'end_year': str(dict['end_year']),
            'num':len(dict2),
            'project_list' : dict2
        })
    

def project_search(request: HttpRequest):
    manager = project()

    if request.method == 'POST':
        project_id = request.POST.dict()['project_number']
        try:
            manager.delete(project_id)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')

    if 'query' in request.GET.dict():
        query = request.GET.dict()['query']
        project_list = []
        try:
            print(query)
            result = manager.search_project_number(query)
            print(result)
            project_list.append(result)
        except:
            pass
        try:
            results = manager.search_project_name(query)
            project_list.extend(results)
        except:
            pass
        return render(request, 'project/search.html', {
            'query': query,
            'num': len(project_list),
            'project_list': project_list
        })
    return render(request, 'project/search.html')

def paper_insert(request: HttpRequest):
    if request.method == 'POST':

        manager = paper()
        data = request.POST.dict()
        data['author_index_list'] = string_to_list(data['author_index_list'])
        
        manager.insert(data)
        subdata = data.copy()
        print(data)
        try:
            for i in data['author_index_list']:
                subdata['job_number'] = data['author_id_' + str(i)]
                subdata['ranking'] = data['author_position_' + str(i)]
                subdata['corresponding_author'] = str2bool(data['corresponding_author_' + str(i)])
                
                # print(subdata)
                manager.insert_publish_paper(subdata)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    return render(request, 'paper/insert.html')

def paper_update(request: HttpRequest):
    manager = paper()
    # print(request.path)
    serial_number = re.search(r'/paper/(\d{1,4})/update', request.path).group(1)
    
    print(serial_number)
    if request.method == 'POST':
        data = request.POST.dict()
        data['serial_number'] = serial_number
        data['author_index_list'] = string_to_list(data['author_index_list'])
        print(data)
        manager.delete(serial_number)
        subdata = data.copy()
        
        try:
            for i in data['author_index_list']:
                subdata['job_number'] = data['author_id_' + str(i)]
                subdata['ranking'] = data['author_position_' + str(i)]
                subdata['corresponding_author'] = str2bool(data['corresponding_author_' + str(i)])
                manager.update_paperself(subdata)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')
    else:
        dict = manager.search_serial_number(serial_number)
        print(dict)
        dict2 = manager.search_teacher(serial_number)
        print(dict2)
        return render(request, 'paper/update.html', {
            'serial_number': dict['serial_number'],
            'paper_name': dict['paper_name'],
            'publish_source': dict['publish_source'],
            'publish_year': str(dict['publish_year']),
            'type': dict['type'],
            'level': dict['level'],
            'num': len(dict2),
            'author_list': dict2
        })

def paper_search(request: HttpRequest):
    manager = paper()
    print(request.GET.dict())

    if request.method == 'POST':
        serial_number = request.POST.dict()['serial_number']
        try:
            manager.delete(serial_number)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success')

    if 'query' in request.GET.dict():
        query = request.GET.dict()['query']
        paper_list = []

        try:
            result = manager.search_serial_number(query)
            paper_list.append(result)
        except:
            pass
        try:
            results = manager.search_paper_name(query)
            paper_list.extend(results)
        except:
            pass
        try:
            results = manager.search_job_number(query)
            paper_list.extend(results)
        except:
            pass
        print(paper_list)
        return render(request, 'paper/search.html', { 'query': query, 'num': len(paper_list), 'paper_list': paper_list })
        
    return render(request, 'paper/search.html')

def teacher_statistic(request: HttpRequest):
    manager1 = teacher()
    manager2 = project()
    manager3 = paper()
    manager4 = course()
    if 'job_number' in request.GET.dict() and 'start_year' in request.GET.dict() and 'end_year' in request.GET.dict():
        job_number = request.GET.dict()['job_number']
        start_year = request.GET.dict()['start_year']
        end_year = request.GET.dict()['end_year']
        try:
            teacher1 = manager1.search_id(job_number)
            print(teacher1)
            project_list = manager2.search_jobnumber_year(job_number, start_year, end_year)
            # print('project_list',project_list)
            course_list = manager4.search_jobnumber_year(job_number, start_year, end_year)
            print('course_list',course_list)
            paper_list = manager3.search_jobnumber_year(job_number, start_year, end_year)
            # print('paper_list',paper_list)
            return render(request, 'statistic.html', {
                'teacher_list': teacher1,
                'project_list': project_list,
                'paper_list': paper_list,
                'course_list': course_list
            })
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'statistic.html')


def index(request: HttpRequest):
    return render(request, 'index.html')


#对项目类型和整数进行转换：1-国家级项目，2-省部级项目，3-市厅级项目，4-企业合作项目，5-其它类型项目。
def project_type_int(project_type):
    if project_type == '国家级项目':
        return 1
    elif project_type == '省部级项目':
        return 2
    elif project_type == '市厅级项目':
        return 3
    elif project_type == '企业合作项目':
        return 4
    elif project_type == '其它类型项目':
        return 5
    else:
        return project_type
    
def string_to_list(s):
    lst = json.loads(s)
    if isinstance(lst, list):
        return lst
    
def str2bool(s):
    if (s == 'off'):
        return False
    if (s == 'on'):
        return True