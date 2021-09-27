function clear_select(select_element) {
    // Remove all current options from a HTML select element
    for (let a in select_element.options) {
        select_element.options.remove(0);
    }
}