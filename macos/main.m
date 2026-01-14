#import <Cocoa/Cocoa.h>
#import "core.h"

void mac_core_setup(void);

// TEMP LOG
void AppendLog(NSString* text) {
    NSLog(@"%@", text);
}

int main() {
    @autoreleasepool {
        mac_core_setup();

        // simulate usage
        core_send_text("Hello from macOS core");

        [[NSRunLoop currentRunLoop] run];
    }
    return 0;
}
