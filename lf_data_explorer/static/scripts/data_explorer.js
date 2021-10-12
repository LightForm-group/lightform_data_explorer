function clear_select(select_element) {
    // Remove all current options from a HTML select element
    for (let a in select_element.options) {
        select_element.options.remove(0);
    }
}

function activate_select_option(select_element, name) {
    // Change the selectedIndex of a select element to the index of the option with text = `name`.
    // If name is not found in the options then do not change the selection.
    for (let i = 0; i < select_element.length; i++) {
        if (select_element[i].text === name) {
            select_element.selectedIndex = i
            break
        }
    }
}