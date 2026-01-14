#include "core.h"
#include <stdio.h>
#include <string.h>

static LogCallback log_cb = 0;
static SendCallback send_cb = 0;

void core_init(LogCallback lcb, SendCallback scb) {
    log_cb = lcb;
    send_cb = scb;
}

void core_send_text(const char* text) {
    if (!send_cb || !log_cb) return;

    char json[1024];
    snprintf(json, sizeof(json),
        "{\"type\":\"text\",\"content\":\"%s\"}", text);

    log_cb("Core: sending text");
    send_cb(json);
}

void core_on_server_message(const char* msg) {
    if (!log_cb) return;
    log_cb(msg);
}
