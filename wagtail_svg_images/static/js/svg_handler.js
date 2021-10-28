// RegexExpressions to find targets and handlers
const choiceHandlerIdRegex = /ag-choice-handler--([a-zA-Z\-\_\d]+)/;
const hiddenIfRegex = new RegExp( 'ag-choice-handler-hidden-if--([a-zA-Z\\-\\_\\d]+)', 'i');

function initHandler(element) {
    const parent = element.closest(".ag-choice-handler");
    const choiceHandlerId = choiceHandlerIdRegex.exec(parent.className)[1];
    const value = element.checked;

    if (!choiceHandlerId) {
        return;
    }
    // Get Targets
    let choiceHandlerTargets = parent.parentElement.querySelectorAll('.ag-choice-handler-target--' + choiceHandlerId);
    if (choiceHandlerTargets.length === 0 ) {
        choiceHandlerTargets = parent.parentElement.parentElement.querySelectorAll('.ag-choice-handler-target--' + choiceHandlerId);
    }
    // Validate Target
    for (let i = 0; i < choiceHandlerTargets.length; i++) {
        let targetElement = choiceHandlerTargets[i];
        let matches = hiddenIfRegex.exec(targetElement.className);
        hiddenIfRegex.lastIndex = 0;
        let hiddenIfValue = matches[1];
        if (targetElement.tagName === "DIV") {
            targetElement = targetElement.parentNode;
        }
        if (String(value) === hiddenIfValue){
            targetElement.classList.add('u-hidden');
        } else {
            targetElement.classList.remove('u-hidden');
        }
    }
}

document.addEventListener("DOMContentLoaded", function (event){
    let element_list = document.getElementsByClassName("ag-choice-handler");
    for (let i=0;i < element_list.length; i++){
        initHandler(element_list[i].querySelectorAll("input")[0]);
    }
});
document.addEventListener("change", function (event){
    initHandler(event.target);
});
