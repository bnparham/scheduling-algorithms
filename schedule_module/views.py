from django.shortcuts import render
from django.views import View

from .assets.main import *

# Create your views here.
class HomeView(View) :
    def get(self, request):
        context = {}
        return render(request, 'schedule_module/home.html', context)
    
    def post(self, request):

        num_dynamic = int(request.POST.get('numDynamic', 0))
        roundRobinInp = int(request.POST.get('roundRobinInp', 0))

        process_li = []
        at_li = []
        cbt_li = []
        total = []
        for i in range(1, num_dynamic + 1):
            process_name = request.POST.get(f'process_{i}')
            at_value = request.POST.get(f'at_{i}')
            cbt_value = request.POST.get(f'cbt_{i}')

            process_li.append(process_name)
            at_li.append(int(at_value))
            cbt_li.append(int(cbt_value))

            total.append({
                'id': i,
                'process_name': process_name,
                'at_value': at_value,
                'cbt_value': cbt_value
            })

        os = OS(
                pd.DataFrame(
                    {"Process" : process_li,
                    "AT" : at_li,
                    "CBT" : cbt_li,
                    }
                )
        )

        schedulingAlgorithm_value = request.POST.get('schedulingAlgorithm')
        match schedulingAlgorithm_value :
            case 'fcfs' :
                os.FCFS()
            case 'spn' :
                os.SPN()
            case 'hrrn' :
                os.HRRN()
            case 'roundRobin':
                os.Round_Robin(roundRobinInp)


        context = {
            'num_dynamic' : num_dynamic,
            'total' : total,
            'roundRobinInp' : roundRobinInp,
        }
        return render(request, 'schedule_module/home.html', context)
