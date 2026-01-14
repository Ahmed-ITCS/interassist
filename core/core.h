#pragma once

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*LogCallback)(const char* text);
typedef void (*SendCallback)(const char* json);

void core_init(LogCallback log_cb, SendCallback send_cb);
void core_send_text(const char* text);
void core_on_server_message(const char* msg);

#ifdef __cplusplus
}
#endif
