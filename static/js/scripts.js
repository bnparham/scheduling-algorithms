// numDynamicInput
var numDynamicInput = document.querySelector('#numDynamic')
var count = 3

// add input

const addProcess = (count) => {

    // Create the process-group HTML structure
    var processGroupHTML = `
        <div class="mb-3">
            <label for="process_${count}" class="form-label">Process ${count}</label>
            <input type="hidden" name="process_${count}" value="P${count}">
            <input required readonly disabled value="P${count}" type="text" class="form-control" id="process_${count}" aria-describedby="emailHelp">
        </div>
        <div class="mb-3">
            <label for="at_${count}" class="form-label">AT ${count}</label>
            <input required type="number" class="form-control" name="at_${count}" id="at_${count}">
        </div>
        <div class="mb-3">
            <label for="cbt_${count}" class="form-label">CBT ${count}</label>
            <input required type="number" class="form-control" name="cbt_${count}" id="cbt_${count}">
        </div>
    `;

    // Create a Div container element
    var DivContainer = document.createElement("div");
    DivContainer.classList.add('col-md-4');

    // Set innerHTML of the container to the processGroupHTML
    DivContainer.innerHTML = processGroupHTML;

    // Get the parent element by its ID
    var parentElement = document.querySelector("#scheduleForm");

    // Append the child element from the container to the parent element
    parentElement.appendChild(DivContainer);
}

const processHandeler = () => {
    count ++
    numDynamicInput.value = count
    addProcess(count)
}

const selectBox = document.querySelector('#schedulingAlgorithm')
selectBox.addEventListener('change',handleSchedulingAlgorithmChange);

const schedulingAlgorithmContainer = document.querySelector('#schedulingAlgorithmContainer')

function handleSchedulingAlgorithmChange() {
    const defaultOpt = document.querySelector('#default-opt');
    defaultOpt.disabled = true;

    // Check if the input element already exists
    const existingInput = document.querySelector('#roundRobinInp');

    if (selectBox.value === 'roundRobin' && !existingInput) {
        // Create a new input element
        const roundRobinInp = document.createElement('input');
        roundRobinInp.required = true;
        roundRobinInp.name = 'roundRobinInp';
        roundRobinInp.id = 'roundRobinInp';
        roundRobinInp.type = 'number';
        roundRobinInp.classList.add('mt-3', 'form-control');
        roundRobinInp.placeholder = 'Assume Time Quantum';

        // Append the input element to the container
        schedulingAlgorithmContainer.appendChild(roundRobinInp);
    } else if (existingInput) {
        // Remove the existing input element
        schedulingAlgorithmContainer.removeChild(existingInput);
    }


    // // Remove the event listener after it has been executed
    // document.querySelector('#schedulingAlgorithm').removeEventListener('change', handleSchedulingAlgorithmChange);
}

document.getElementById('refreshButton').addEventListener('click', function() {
    location.reload();
});