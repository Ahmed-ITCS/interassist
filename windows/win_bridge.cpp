#include "core.h"
#include <windows.h>
#include <stdio.h>

void win_log(const char* text) {
    printf("[LOG] %s\n", text);
}

void win_send(const char* json) {
    // send via WinHTTP / websocket library
    printf("[SEND] %s\n", json);
}

void win_core_setup() {
    core_init(win_log, win_send);
}
