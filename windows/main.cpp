#include "core.h"

void win_core_setup();

int main() {
    win_core_setup();
    core_send_text("Hello from Windows");
    return 0;
}
