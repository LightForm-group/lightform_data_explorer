function clear_select(select_element) {
    for (let a in select_element.options) {
        select_element.options.remove(0);
    }
}