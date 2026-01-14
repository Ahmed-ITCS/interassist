#import <Cocoa/Cocoa.h>
#import "core.h"

// ---- forward decls from your existing code ----
extern void AppendLog(NSString* text);
extern NSURLSessionWebSocketTask* ws;

// ---- bridge functions ----
void mac_log(const char* text) {
    dispatch_async(dispatch_get_main_queue(), ^{
        AppendLog([NSString stringWithUTF8String:text]);
    });
}

void mac_send(const char* json) {
    NSString* str = [NSString stringWithUTF8String:json];
    NSURLSessionWebSocketMessage* msg =
        [[NSURLSessionWebSocketMessage alloc] initWithString:str];

    [ws sendMessage:msg completionHandler:nil];
}

void mac_core_setup(void) {
    core_init(mac_log, mac_send);
}
