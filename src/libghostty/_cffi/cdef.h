/* Curated CFFI ABI surface for libghostty-vt.

   This file intentionally declares only the types, constants, and functions
   used by the Python wrappers. The upstream Ghostty commit this surface targets
   is recorded in pyproject.toml under tool.libghostty. */

typedef enum {
    GHOSTTY_SUCCESS       =  0,
    GHOSTTY_OUT_OF_MEMORY = -1,
    GHOSTTY_INVALID_VALUE = -2,
    GHOSTTY_OUT_OF_SPACE  = -3,
    GHOSTTY_NO_VALUE      = -4,
} GhosttyResult;

typedef uint16_t GhosttyMode;
typedef uint16_t GhosttyMods;
typedef uint8_t  GhosttyColorPaletteIndex;
typedef uint8_t  GhosttyKittyKeyFlags;

typedef struct GhosttyAllocator GhosttyAllocator;
typedef struct GhosttyFormatterImpl *GhosttyFormatter;
typedef struct GhosttyKeyEncoderImpl *GhosttyKeyEncoder;
typedef struct GhosttyKeyEventImpl *GhosttyKeyEvent;
typedef struct GhosttyKittyGraphicsImpl *GhosttyKittyGraphics;
typedef const struct GhosttyKittyGraphicsImageImpl *GhosttyKittyGraphicsImage;
typedef struct GhosttyKittyGraphicsPlacementIteratorImpl *GhosttyKittyGraphicsPlacementIterator;
typedef struct GhosttyMouseEncoderImpl *GhosttyMouseEncoder;
typedef struct GhosttyMouseEventImpl *GhosttyMouseEvent;
typedef struct GhosttyOscCommandImpl *GhosttyOscCommand;
typedef struct GhosttyOscParserImpl *GhosttyOscParser;
typedef struct GhosttyRenderStateImpl *GhosttyRenderState;
typedef struct GhosttyRenderStateRowCellsImpl *GhosttyRenderStateRowCells;
typedef struct GhosttyRenderStateRowIteratorImpl *GhosttyRenderStateRowIterator;
typedef struct GhosttySelection GhosttySelection;
typedef struct GhosttySgrParserImpl *GhosttySgrParser;
typedef struct GhosttyTerminalImpl *GhosttyTerminal;

typedef struct {
    const uint8_t *ptr;
    size_t len;
} GhosttyString;

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} GhosttyColorRgb;

void ghostty_free(const GhosttyAllocator *allocator, uint8_t *ptr, size_t len);

typedef enum {
    GHOSTTY_BUILD_INFO_SIMD = 1,
    GHOSTTY_BUILD_INFO_KITTY_GRAPHICS = 2,
    GHOSTTY_BUILD_INFO_TMUX_CONTROL_MODE = 3,
    GHOSTTY_BUILD_INFO_VERSION_STRING = 5,
    GHOSTTY_BUILD_INFO_VERSION_MAJOR = 6,
    GHOSTTY_BUILD_INFO_VERSION_MINOR = 7,
    GHOSTTY_BUILD_INFO_VERSION_PATCH = 8,
} GhosttyBuildInfo;

GhosttyResult ghostty_build_info(GhosttyBuildInfo data, void *out);

typedef struct {
    uint16_t cols;
    uint16_t rows;
    size_t max_scrollback;
} GhosttyTerminalOptions;

typedef enum {
    GHOSTTY_SCROLL_VIEWPORT_TOP = 0,
    GHOSTTY_SCROLL_VIEWPORT_BOTTOM = 1,
    GHOSTTY_SCROLL_VIEWPORT_DELTA = 2,
} GhosttyTerminalScrollViewportTag;

typedef union {
    intptr_t delta;
    uint64_t _padding[2];
} GhosttyTerminalScrollViewportValue;

typedef struct {
    GhosttyTerminalScrollViewportTag tag;
    GhosttyTerminalScrollViewportValue value;
} GhosttyTerminalScrollViewport;

typedef enum {
    GHOSTTY_TERMINAL_SCREEN_ALTERNATE = 1,
} GhosttyTerminalScreen;

typedef enum {
    GHOSTTY_TERMINAL_OPT_WRITE_PTY = 1,
    GHOSTTY_TERMINAL_OPT_SIZE = 6,
    GHOSTTY_TERMINAL_OPT_DEVICE_ATTRIBUTES = 8,
    GHOSTTY_TERMINAL_OPT_COLOR_FOREGROUND = 11,
    GHOSTTY_TERMINAL_OPT_COLOR_BACKGROUND = 12,
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_STORAGE_LIMIT = 15,
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_FILE = 16,
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_TEMP_FILE = 17,
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_SHARED_MEM = 18,
    GHOSTTY_TERMINAL_OPT_APC_MAX_BYTES = 19,
    GHOSTTY_TERMINAL_OPT_APC_MAX_BYTES_KITTY = 20,
} GhosttyTerminalOption;

typedef enum {
    GHOSTTY_TERMINAL_DATA_COLS = 1,
    GHOSTTY_TERMINAL_DATA_ROWS = 2,
    GHOSTTY_TERMINAL_DATA_CURSOR_X = 3,
    GHOSTTY_TERMINAL_DATA_CURSOR_Y = 4,
    GHOSTTY_TERMINAL_DATA_ACTIVE_SCREEN = 6,
    GHOSTTY_TERMINAL_DATA_CURSOR_VISIBLE = 7,
    GHOSTTY_TERMINAL_DATA_TITLE = 12,
    GHOSTTY_TERMINAL_DATA_TOTAL_ROWS = 14,
    GHOSTTY_TERMINAL_DATA_SCROLLBACK_ROWS = 15,
    GHOSTTY_TERMINAL_DATA_COLOR_FOREGROUND = 18,
    GHOSTTY_TERMINAL_DATA_COLOR_BACKGROUND = 19,
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_STORAGE_LIMIT = 26,
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_FILE = 27,
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_TEMP_FILE = 28,
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_SHARED_MEM = 29,
    GHOSTTY_TERMINAL_DATA_KITTY_GRAPHICS = 30,
} GhosttyTerminalData;

GhosttyResult ghostty_terminal_new(const GhosttyAllocator *allocator,
                                   GhosttyTerminal *terminal,
                                   GhosttyTerminalOptions options);
void ghostty_terminal_free(GhosttyTerminal terminal);
void ghostty_terminal_reset(GhosttyTerminal terminal);
GhosttyResult ghostty_terminal_resize(GhosttyTerminal terminal,
                                      uint16_t cols,
                                      uint16_t rows,
                                      uint32_t cell_width_px,
                                      uint32_t cell_height_px);
GhosttyResult ghostty_terminal_set(GhosttyTerminal terminal,
                                   GhosttyTerminalOption option,
                                   const void *value);
void ghostty_terminal_vt_write(GhosttyTerminal terminal, const uint8_t *data, size_t len);
void ghostty_terminal_scroll_viewport(GhosttyTerminal terminal,
                                      GhosttyTerminalScrollViewport behavior);
GhosttyResult ghostty_terminal_mode_get(GhosttyTerminal terminal,
                                        GhosttyMode mode,
                                        bool *out_value);
GhosttyResult ghostty_terminal_mode_set(GhosttyTerminal terminal, GhosttyMode mode, bool value);
GhosttyResult ghostty_terminal_get(GhosttyTerminal terminal, GhosttyTerminalData data, void *out);

typedef struct {
    uint16_t conformance_level;
    uint16_t features[64];
    size_t num_features;
} GhosttyDeviceAttributesPrimary;

typedef struct {
    uint16_t device_type;
    uint16_t firmware_version;
    uint16_t rom_cartridge;
} GhosttyDeviceAttributesSecondary;

typedef struct {
    uint32_t unit_id;
} GhosttyDeviceAttributesTertiary;

typedef struct {
    GhosttyDeviceAttributesPrimary primary;
    GhosttyDeviceAttributesSecondary secondary;
    GhosttyDeviceAttributesTertiary tertiary;
} GhosttyDeviceAttributes;

typedef struct {
    uint16_t rows;
    uint16_t columns;
    uint32_t cell_width;
    uint32_t cell_height;
} GhosttySizeReportSize;

typedef void (*GhosttyTerminalWritePtyFn)(GhosttyTerminal terminal,
                                          void *userdata,
                                          const uint8_t *data,
                                          size_t len);
typedef bool (*GhosttyTerminalSizeFn)(GhosttyTerminal terminal,
                                      void *userdata,
                                      GhosttySizeReportSize *out_size);
typedef bool (*GhosttyTerminalDeviceAttributesFn)(GhosttyTerminal terminal,
                                                   void *userdata,
                                                   GhosttyDeviceAttributes *out_attrs);

bool ghostty_paste_is_safe(const char *data, size_t len);
GhosttyResult ghostty_paste_encode(char *data,
                                   size_t data_len,
                                   bool bracketed,
                                   char *buf,
                                   size_t buf_len,
                                   size_t *out_written);

typedef enum {
    GHOSTTY_SGR_ATTR_UNDERLINE = 7,
    GHOSTTY_SGR_ATTR_UNDERLINE_COLOR = 8,
    GHOSTTY_SGR_ATTR_UNDERLINE_COLOR_256 = 9,
    GHOSTTY_SGR_ATTR_DIRECT_COLOR_FG = 21,
    GHOSTTY_SGR_ATTR_DIRECT_COLOR_BG = 22,
    GHOSTTY_SGR_ATTR_BG_8 = 23,
    GHOSTTY_SGR_ATTR_FG_8 = 24,
    GHOSTTY_SGR_ATTR_BRIGHT_BG_8 = 27,
    GHOSTTY_SGR_ATTR_BRIGHT_FG_8 = 28,
    GHOSTTY_SGR_ATTR_BG_256 = 29,
    GHOSTTY_SGR_ATTR_FG_256 = 30,
} GhosttySgrAttributeTag;

typedef int GhosttySgrUnderline;

typedef union {
    GhosttySgrUnderline underline;
    GhosttyColorRgb underline_color;
    GhosttyColorPaletteIndex underline_color_256;
    GhosttyColorRgb direct_color_fg;
    GhosttyColorRgb direct_color_bg;
    GhosttyColorPaletteIndex bg_8;
    GhosttyColorPaletteIndex fg_8;
    GhosttyColorPaletteIndex bright_bg_8;
    GhosttyColorPaletteIndex bright_fg_8;
    GhosttyColorPaletteIndex bg_256;
    GhosttyColorPaletteIndex fg_256;
    uint64_t _padding[8];
} GhosttySgrAttributeValue;

typedef struct {
    GhosttySgrAttributeTag tag;
    GhosttySgrAttributeValue value;
} GhosttySgrAttribute;

GhosttyResult ghostty_sgr_new(const GhosttyAllocator *allocator, GhosttySgrParser *parser);
void ghostty_sgr_free(GhosttySgrParser parser);
GhosttyResult ghostty_sgr_set_params(GhosttySgrParser parser,
                                     const uint16_t *params,
                                     const char *separators,
                                     size_t len);
bool ghostty_sgr_next(GhosttySgrParser parser, GhosttySgrAttribute *attr);

typedef enum {
    GHOSTTY_OSC_COMMAND_INVALID = 0,
    GHOSTTY_OSC_COMMAND_CHANGE_WINDOW_TITLE = 1,
} GhosttyOscCommandType;

typedef enum {
    GHOSTTY_OSC_DATA_CHANGE_WINDOW_TITLE_STR = 1,
} GhosttyOscCommandData;

GhosttyResult ghostty_osc_new(const GhosttyAllocator *allocator, GhosttyOscParser *parser);
void ghostty_osc_free(GhosttyOscParser parser);
void ghostty_osc_reset(GhosttyOscParser parser);
void ghostty_osc_next(GhosttyOscParser parser, uint8_t byte);
GhosttyOscCommand ghostty_osc_end(GhosttyOscParser parser, uint8_t terminator);
GhosttyOscCommandType ghostty_osc_command_type(GhosttyOscCommand command);
bool ghostty_osc_command_data(GhosttyOscCommand command, GhosttyOscCommandData data, void *out);

typedef enum {
    GHOSTTY_KEY_ACTION_RELEASE = 0,
    GHOSTTY_KEY_ACTION_PRESS = 1,
    GHOSTTY_KEY_ACTION_REPEAT = 2,
} GhosttyKeyAction;

typedef enum {
    GHOSTTY_KEY_ENCODER_OPT_CURSOR_KEY_APPLICATION = 0,
    GHOSTTY_KEY_ENCODER_OPT_KEYPAD_KEY_APPLICATION = 1,
    GHOSTTY_KEY_ENCODER_OPT_IGNORE_KEYPAD_WITH_NUMLOCK = 2,
    GHOSTTY_KEY_ENCODER_OPT_ALT_ESC_PREFIX = 3,
    GHOSTTY_KEY_ENCODER_OPT_MODIFY_OTHER_KEYS_STATE_2 = 4,
    GHOSTTY_KEY_ENCODER_OPT_KITTY_FLAGS = 5,
    GHOSTTY_KEY_ENCODER_OPT_MACOS_OPTION_AS_ALT = 6,
    GHOSTTY_KEY_ENCODER_OPT_BACKARROW_KEY_MODE = 7,
    GHOSTTY_KEY_ENCODER_OPT_MAX_VALUE = 0x7fffffff,
} GhosttyKeyEncoderOption;

typedef enum {
    GHOSTTY_KEY_UNIDENTIFIED,
    GHOSTTY_KEY_BACKQUOTE,
    GHOSTTY_KEY_BACKSLASH,
    GHOSTTY_KEY_BRACKET_LEFT,
    GHOSTTY_KEY_BRACKET_RIGHT,
    GHOSTTY_KEY_COMMA,
    GHOSTTY_KEY_DIGIT_0,
    GHOSTTY_KEY_DIGIT_1,
    GHOSTTY_KEY_DIGIT_2,
    GHOSTTY_KEY_DIGIT_3,
    GHOSTTY_KEY_DIGIT_4,
    GHOSTTY_KEY_DIGIT_5,
    GHOSTTY_KEY_DIGIT_6,
    GHOSTTY_KEY_DIGIT_7,
    GHOSTTY_KEY_DIGIT_8,
    GHOSTTY_KEY_DIGIT_9,
    GHOSTTY_KEY_EQUAL,
    GHOSTTY_KEY_INTL_BACKSLASH,
    GHOSTTY_KEY_INTL_RO,
    GHOSTTY_KEY_INTL_YEN,
    GHOSTTY_KEY_A,
    GHOSTTY_KEY_B,
    GHOSTTY_KEY_C,
    GHOSTTY_KEY_D,
    GHOSTTY_KEY_E,
    GHOSTTY_KEY_F,
    GHOSTTY_KEY_G,
    GHOSTTY_KEY_H,
    GHOSTTY_KEY_I,
    GHOSTTY_KEY_J,
    GHOSTTY_KEY_K,
    GHOSTTY_KEY_L,
    GHOSTTY_KEY_M,
    GHOSTTY_KEY_N,
    GHOSTTY_KEY_O,
    GHOSTTY_KEY_P,
    GHOSTTY_KEY_Q,
    GHOSTTY_KEY_R,
    GHOSTTY_KEY_S,
    GHOSTTY_KEY_T,
    GHOSTTY_KEY_U,
    GHOSTTY_KEY_V,
    GHOSTTY_KEY_W,
    GHOSTTY_KEY_X,
    GHOSTTY_KEY_Y,
    GHOSTTY_KEY_Z,
    GHOSTTY_KEY_MINUS,
    GHOSTTY_KEY_PERIOD,
    GHOSTTY_KEY_QUOTE,
    GHOSTTY_KEY_SEMICOLON,
    GHOSTTY_KEY_SLASH,
    GHOSTTY_KEY_ALT_LEFT,
    GHOSTTY_KEY_ALT_RIGHT,
    GHOSTTY_KEY_BACKSPACE,
    GHOSTTY_KEY_CAPS_LOCK,
    GHOSTTY_KEY_CONTEXT_MENU,
    GHOSTTY_KEY_CONTROL_LEFT,
    GHOSTTY_KEY_CONTROL_RIGHT,
    GHOSTTY_KEY_ENTER,
    GHOSTTY_KEY_META_LEFT,
    GHOSTTY_KEY_META_RIGHT,
    GHOSTTY_KEY_SHIFT_LEFT,
    GHOSTTY_KEY_SHIFT_RIGHT,
    GHOSTTY_KEY_SPACE,
    GHOSTTY_KEY_TAB,
    GHOSTTY_KEY_CONVERT,
    GHOSTTY_KEY_KANA_MODE,
    GHOSTTY_KEY_NON_CONVERT,
    GHOSTTY_KEY_DELETE,
    GHOSTTY_KEY_END,
    GHOSTTY_KEY_HELP,
    GHOSTTY_KEY_HOME,
    GHOSTTY_KEY_INSERT,
    GHOSTTY_KEY_PAGE_DOWN,
    GHOSTTY_KEY_PAGE_UP,
    GHOSTTY_KEY_ARROW_DOWN,
    GHOSTTY_KEY_ARROW_LEFT,
    GHOSTTY_KEY_ARROW_RIGHT,
    GHOSTTY_KEY_ARROW_UP,
    GHOSTTY_KEY_NUM_LOCK,
    GHOSTTY_KEY_NUMPAD_0,
    GHOSTTY_KEY_NUMPAD_1,
    GHOSTTY_KEY_NUMPAD_2,
    GHOSTTY_KEY_NUMPAD_3,
    GHOSTTY_KEY_NUMPAD_4,
    GHOSTTY_KEY_NUMPAD_5,
    GHOSTTY_KEY_NUMPAD_6,
    GHOSTTY_KEY_NUMPAD_7,
    GHOSTTY_KEY_NUMPAD_8,
    GHOSTTY_KEY_NUMPAD_9,
    GHOSTTY_KEY_NUMPAD_ADD,
    GHOSTTY_KEY_NUMPAD_BACKSPACE,
    GHOSTTY_KEY_NUMPAD_CLEAR,
    GHOSTTY_KEY_NUMPAD_CLEAR_ENTRY,
    GHOSTTY_KEY_NUMPAD_COMMA,
    GHOSTTY_KEY_NUMPAD_DECIMAL,
    GHOSTTY_KEY_NUMPAD_DIVIDE,
    GHOSTTY_KEY_NUMPAD_ENTER,
    GHOSTTY_KEY_NUMPAD_EQUAL,
    GHOSTTY_KEY_NUMPAD_MEMORY_ADD,
    GHOSTTY_KEY_NUMPAD_MEMORY_CLEAR,
    GHOSTTY_KEY_NUMPAD_MEMORY_RECALL,
    GHOSTTY_KEY_NUMPAD_MEMORY_STORE,
    GHOSTTY_KEY_NUMPAD_MEMORY_SUBTRACT,
    GHOSTTY_KEY_NUMPAD_MULTIPLY,
    GHOSTTY_KEY_NUMPAD_PAREN_LEFT,
    GHOSTTY_KEY_NUMPAD_PAREN_RIGHT,
    GHOSTTY_KEY_NUMPAD_SUBTRACT,
    GHOSTTY_KEY_NUMPAD_SEPARATOR,
    GHOSTTY_KEY_NUMPAD_UP,
    GHOSTTY_KEY_NUMPAD_DOWN,
    GHOSTTY_KEY_NUMPAD_RIGHT,
    GHOSTTY_KEY_NUMPAD_LEFT,
    GHOSTTY_KEY_NUMPAD_BEGIN,
    GHOSTTY_KEY_NUMPAD_HOME,
    GHOSTTY_KEY_NUMPAD_END,
    GHOSTTY_KEY_NUMPAD_INSERT,
    GHOSTTY_KEY_NUMPAD_DELETE,
    GHOSTTY_KEY_NUMPAD_PAGE_UP,
    GHOSTTY_KEY_NUMPAD_PAGE_DOWN,
    GHOSTTY_KEY_ESCAPE,
    GHOSTTY_KEY_F1,
    GHOSTTY_KEY_F2,
    GHOSTTY_KEY_F3,
    GHOSTTY_KEY_F4,
    GHOSTTY_KEY_F5,
    GHOSTTY_KEY_F6,
    GHOSTTY_KEY_F7,
    GHOSTTY_KEY_F8,
    GHOSTTY_KEY_F9,
    GHOSTTY_KEY_F10,
    GHOSTTY_KEY_F11,
    GHOSTTY_KEY_F12,
} GhosttyKey;

GhosttyResult ghostty_key_event_new(const GhosttyAllocator *allocator, GhosttyKeyEvent *event);
void ghostty_key_event_free(GhosttyKeyEvent event);
void ghostty_key_event_set_action(GhosttyKeyEvent event, GhosttyKeyAction action);
GhosttyKeyAction ghostty_key_event_get_action(GhosttyKeyEvent event);
void ghostty_key_event_set_key(GhosttyKeyEvent event, GhosttyKey key);
GhosttyKey ghostty_key_event_get_key(GhosttyKeyEvent event);
void ghostty_key_event_set_mods(GhosttyKeyEvent event, GhosttyMods mods);
GhosttyMods ghostty_key_event_get_mods(GhosttyKeyEvent event);
void ghostty_key_event_set_consumed_mods(GhosttyKeyEvent event, GhosttyMods consumed_mods);
GhosttyMods ghostty_key_event_get_consumed_mods(GhosttyKeyEvent event);
void ghostty_key_event_set_composing(GhosttyKeyEvent event, bool composing);
bool ghostty_key_event_get_composing(GhosttyKeyEvent event);
void ghostty_key_event_set_utf8(GhosttyKeyEvent event, const char *utf8, size_t len);
const char *ghostty_key_event_get_utf8(GhosttyKeyEvent event, size_t *len);
void ghostty_key_event_set_unshifted_codepoint(GhosttyKeyEvent event, uint32_t codepoint);
uint32_t ghostty_key_event_get_unshifted_codepoint(GhosttyKeyEvent event);

GhosttyResult ghostty_key_encoder_new(const GhosttyAllocator *allocator,
                                      GhosttyKeyEncoder *encoder);
void ghostty_key_encoder_free(GhosttyKeyEncoder encoder);
void ghostty_key_encoder_setopt_from_terminal(GhosttyKeyEncoder encoder,
                                              GhosttyTerminal terminal);
void ghostty_key_encoder_setopt(GhosttyKeyEncoder encoder,
                                GhosttyKeyEncoderOption option,
                                const void *value);
GhosttyResult ghostty_key_encoder_encode(GhosttyKeyEncoder encoder,
                                         GhosttyKeyEvent event,
                                         char *out_buf,
                                         size_t out_buf_size,
                                         size_t *out_len);

typedef int GhosttyMouseAction;
typedef int GhosttyMouseButton;

typedef struct {
    float x;
    float y;
} GhosttyMousePosition;

GhosttyResult ghostty_mouse_event_new(const GhosttyAllocator *allocator,
                                      GhosttyMouseEvent *event);
void ghostty_mouse_event_free(GhosttyMouseEvent event);
void ghostty_mouse_event_set_action(GhosttyMouseEvent event, GhosttyMouseAction action);
GhosttyMouseAction ghostty_mouse_event_get_action(GhosttyMouseEvent event);
void ghostty_mouse_event_set_button(GhosttyMouseEvent event, GhosttyMouseButton button);
void ghostty_mouse_event_clear_button(GhosttyMouseEvent event);
void ghostty_mouse_event_set_mods(GhosttyMouseEvent event, GhosttyMods mods);
GhosttyMods ghostty_mouse_event_get_mods(GhosttyMouseEvent event);
void ghostty_mouse_event_set_position(GhosttyMouseEvent event, GhosttyMousePosition position);
GhosttyMousePosition ghostty_mouse_event_get_position(GhosttyMouseEvent event);

GhosttyResult ghostty_mouse_encoder_new(const GhosttyAllocator *allocator,
                                        GhosttyMouseEncoder *encoder);
void ghostty_mouse_encoder_free(GhosttyMouseEncoder encoder);
void ghostty_mouse_encoder_setopt_from_terminal(GhosttyMouseEncoder encoder,
                                                GhosttyTerminal terminal);
void ghostty_mouse_encoder_reset(GhosttyMouseEncoder encoder);
GhosttyResult ghostty_mouse_encoder_encode(GhosttyMouseEncoder encoder,
                                           GhosttyMouseEvent event,
                                           char *out_buf,
                                           size_t out_buf_size,
                                           size_t *out_len);

typedef enum {
    GHOSTTY_KITTY_GRAPHICS_DATA_INVALID = 0,
    GHOSTTY_KITTY_GRAPHICS_DATA_PLACEMENT_ITERATOR = 1,
    GHOSTTY_KITTY_GRAPHICS_DATA_MAX_VALUE = 0x7fffffff,
} GhosttyKittyGraphicsData;

typedef enum {
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_INVALID = 0,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_IMAGE_ID = 1,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_PLACEMENT_ID = 2,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_IS_VIRTUAL = 3,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_X_OFFSET = 4,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_Y_OFFSET = 5,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_X = 6,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_Y = 7,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_WIDTH = 8,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_HEIGHT = 9,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_COLUMNS = 10,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_ROWS = 11,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_Z = 12,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_MAX_VALUE = 0x7fffffff,
} GhosttyKittyGraphicsPlacementData;

typedef enum {
    GHOSTTY_KITTY_PLACEMENT_LAYER_ALL = 0,
    GHOSTTY_KITTY_PLACEMENT_LAYER_BELOW_BG = 1,
    GHOSTTY_KITTY_PLACEMENT_LAYER_BELOW_TEXT = 2,
    GHOSTTY_KITTY_PLACEMENT_LAYER_ABOVE_TEXT = 3,
    GHOSTTY_KITTY_PLACEMENT_LAYER_MAX_VALUE = 0x7fffffff,
} GhosttyKittyPlacementLayer;

typedef enum {
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_ITERATOR_OPTION_LAYER = 0,
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_ITERATOR_OPTION_MAX_VALUE = 0x7fffffff,
} GhosttyKittyGraphicsPlacementIteratorOption;

typedef enum {
    GHOSTTY_KITTY_IMAGE_FORMAT_RGB = 0,
    GHOSTTY_KITTY_IMAGE_FORMAT_RGBA = 1,
    GHOSTTY_KITTY_IMAGE_FORMAT_PNG = 2,
    GHOSTTY_KITTY_IMAGE_FORMAT_GRAY_ALPHA = 3,
    GHOSTTY_KITTY_IMAGE_FORMAT_GRAY = 4,
    GHOSTTY_KITTY_IMAGE_FORMAT_MAX_VALUE = 0x7fffffff,
} GhosttyKittyImageFormat;

typedef enum {
    GHOSTTY_KITTY_IMAGE_COMPRESSION_NONE = 0,
    GHOSTTY_KITTY_IMAGE_COMPRESSION_ZLIB_DEFLATE = 1,
    GHOSTTY_KITTY_IMAGE_COMPRESSION_MAX_VALUE = 0x7fffffff,
} GhosttyKittyImageCompression;

typedef enum {
    GHOSTTY_KITTY_IMAGE_DATA_INVALID = 0,
    GHOSTTY_KITTY_IMAGE_DATA_ID = 1,
    GHOSTTY_KITTY_IMAGE_DATA_NUMBER = 2,
    GHOSTTY_KITTY_IMAGE_DATA_WIDTH = 3,
    GHOSTTY_KITTY_IMAGE_DATA_HEIGHT = 4,
    GHOSTTY_KITTY_IMAGE_DATA_FORMAT = 5,
    GHOSTTY_KITTY_IMAGE_DATA_COMPRESSION = 6,
    GHOSTTY_KITTY_IMAGE_DATA_DATA_PTR = 7,
    GHOSTTY_KITTY_IMAGE_DATA_DATA_LEN = 8,
    GHOSTTY_KITTY_IMAGE_DATA_MAX_VALUE = 0x7fffffff,
} GhosttyKittyGraphicsImageData;

typedef struct {
    size_t size;
    uint32_t pixel_width;
    uint32_t pixel_height;
    uint32_t grid_cols;
    uint32_t grid_rows;
    int32_t viewport_col;
    int32_t viewport_row;
    bool viewport_visible;
    uint32_t source_x;
    uint32_t source_y;
    uint32_t source_width;
    uint32_t source_height;
} GhosttyKittyGraphicsPlacementRenderInfo;

GhosttyResult ghostty_kitty_graphics_get(GhosttyKittyGraphics graphics,
                                         GhosttyKittyGraphicsData data,
                                         void *out);
GhosttyKittyGraphicsImage ghostty_kitty_graphics_image(GhosttyKittyGraphics graphics,
                                                       uint32_t image_id);
GhosttyResult ghostty_kitty_graphics_image_get(GhosttyKittyGraphicsImage image,
                                               GhosttyKittyGraphicsImageData data,
                                               void *out);
GhosttyResult ghostty_kitty_graphics_image_get_multi(GhosttyKittyGraphicsImage image,
                                                     size_t count,
                                                     const GhosttyKittyGraphicsImageData *keys,
                                                     void **values,
                                                     size_t *out_written);
GhosttyResult ghostty_kitty_graphics_placement_iterator_new(const GhosttyAllocator *allocator,
                                                            GhosttyKittyGraphicsPlacementIterator *out_iterator);
void ghostty_kitty_graphics_placement_iterator_free(GhosttyKittyGraphicsPlacementIterator iterator);
GhosttyResult ghostty_kitty_graphics_placement_iterator_set(GhosttyKittyGraphicsPlacementIterator iterator,
                                                            GhosttyKittyGraphicsPlacementIteratorOption option,
                                                            const void *value);
bool ghostty_kitty_graphics_placement_next(GhosttyKittyGraphicsPlacementIterator iterator);
GhosttyResult ghostty_kitty_graphics_placement_get(GhosttyKittyGraphicsPlacementIterator iterator,
                                                   GhosttyKittyGraphicsPlacementData data,
                                                   void *out);
GhosttyResult ghostty_kitty_graphics_placement_get_multi(GhosttyKittyGraphicsPlacementIterator iterator,
                                                         size_t count,
                                                         const GhosttyKittyGraphicsPlacementData *keys,
                                                         void **values,
                                                         size_t *out_written);
GhosttyResult ghostty_kitty_graphics_placement_rect(GhosttyKittyGraphicsPlacementIterator iterator,
                                                    GhosttyKittyGraphicsImage image,
                                                    GhosttyTerminal terminal,
                                                    GhosttySelection *out_selection);
GhosttyResult ghostty_kitty_graphics_placement_pixel_size(GhosttyKittyGraphicsPlacementIterator iterator,
                                                          GhosttyKittyGraphicsImage image,
                                                          GhosttyTerminal terminal,
                                                          uint32_t *out_width,
                                                          uint32_t *out_height);
GhosttyResult ghostty_kitty_graphics_placement_grid_size(GhosttyKittyGraphicsPlacementIterator iterator,
                                                         GhosttyKittyGraphicsImage image,
                                                         GhosttyTerminal terminal,
                                                         uint32_t *out_cols,
                                                         uint32_t *out_rows);
GhosttyResult ghostty_kitty_graphics_placement_viewport_pos(GhosttyKittyGraphicsPlacementIterator iterator,
                                                            GhosttyKittyGraphicsImage image,
                                                            GhosttyTerminal terminal,
                                                            int32_t *out_col,
                                                            int32_t *out_row);
GhosttyResult ghostty_kitty_graphics_placement_source_rect(GhosttyKittyGraphicsPlacementIterator iterator,
                                                           GhosttyKittyGraphicsImage image,
                                                           uint32_t *out_x,
                                                           uint32_t *out_y,
                                                           uint32_t *out_width,
                                                           uint32_t *out_height);
GhosttyResult ghostty_kitty_graphics_placement_render_info(GhosttyKittyGraphicsPlacementIterator iterator,
                                                           GhosttyKittyGraphicsImage image,
                                                           GhosttyTerminal terminal,
                                                           GhosttyKittyGraphicsPlacementRenderInfo *out_info);

typedef enum {
    GHOSTTY_FORMATTER_FORMAT_PLAIN = 0,
    GHOSTTY_FORMATTER_FORMAT_VT = 1,
    GHOSTTY_FORMATTER_FORMAT_HTML = 2,
} GhosttyFormatterFormat;

typedef struct {
    size_t size;
    bool cursor;
    bool style;
    bool hyperlink;
    bool protection;
    bool kitty_keyboard;
    bool charsets;
} GhosttyFormatterScreenExtra;

typedef struct {
    size_t size;
    bool palette;
    bool modes;
    bool scrolling_region;
    bool tabstops;
    bool pwd;
    bool keyboard;
    GhosttyFormatterScreenExtra screen;
} GhosttyFormatterTerminalExtra;

typedef struct {
    size_t size;
    GhosttyFormatterFormat emit;
    bool unwrap;
    bool trim;
    GhosttyFormatterTerminalExtra extra;
    const GhosttySelection *selection;
} GhosttyFormatterTerminalOptions;

GhosttyResult ghostty_formatter_terminal_new(const GhosttyAllocator *allocator,
                                             GhosttyFormatter *formatter,
                                             GhosttyTerminal terminal,
                                             GhosttyFormatterTerminalOptions options);
GhosttyResult ghostty_formatter_format_alloc(GhosttyFormatter formatter,
                                             const GhosttyAllocator *allocator,
                                             uint8_t **out_ptr,
                                             size_t *out_len);
void ghostty_formatter_free(GhosttyFormatter formatter);

typedef int GhosttyRenderStateDirty;
typedef int GhosttyRenderStateCursorVisualStyle;

typedef enum {
    GHOSTTY_RENDER_STATE_DATA_DIRTY = 3,
    GHOSTTY_RENDER_STATE_DATA_ROW_ITERATOR = 4,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VISUAL_STYLE = 10,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VISIBLE = 11,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_BLINKING = 12,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_HAS_VALUE = 14,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_X = 15,
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_Y = 16,
} GhosttyRenderStateData;

typedef enum {
    GHOSTTY_RENDER_STATE_OPTION_DIRTY = 0,
} GhosttyRenderStateOption;

typedef enum {
    GHOSTTY_RENDER_STATE_ROW_DATA_DIRTY = 1,
    GHOSTTY_RENDER_STATE_ROW_DATA_CELLS = 3,
} GhosttyRenderStateRowData;

typedef enum {
    GHOSTTY_RENDER_STATE_ROW_OPTION_DIRTY = 0,
} GhosttyRenderStateRowOption;

typedef enum {
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_STYLE = 2,
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_LEN = 3,
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_BUF = 4,
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_BG_COLOR = 5,
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_FG_COLOR = 6,
} GhosttyRenderStateRowCellsData;

typedef int GhosttyStyleColorTag;

typedef union {
    GhosttyColorPaletteIndex palette;
    GhosttyColorRgb rgb;
    uint64_t _padding;
} GhosttyStyleColorValue;

typedef struct {
    GhosttyStyleColorTag tag;
    GhosttyStyleColorValue value;
} GhosttyStyleColor;

typedef struct {
    size_t size;
    GhosttyStyleColor fg_color;
    GhosttyStyleColor bg_color;
    GhosttyStyleColor underline_color;
    bool bold;
    bool italic;
    bool faint;
    bool blink;
    bool inverse;
    bool invisible;
    bool strikethrough;
    bool overline;
    int underline;
} GhosttyStyle;

typedef struct {
    size_t size;
    GhosttyColorRgb background;
    GhosttyColorRgb foreground;
    GhosttyColorRgb cursor;
    bool cursor_has_value;
    GhosttyColorRgb palette[256];
} GhosttyRenderStateColors;

GhosttyResult ghostty_render_state_new(const GhosttyAllocator *allocator,
                                       GhosttyRenderState *state);
void ghostty_render_state_free(GhosttyRenderState state);
GhosttyResult ghostty_render_state_update(GhosttyRenderState state, GhosttyTerminal terminal);
GhosttyResult ghostty_render_state_get(GhosttyRenderState state,
                                       GhosttyRenderStateData data,
                                       void *out);
GhosttyResult ghostty_render_state_set(GhosttyRenderState state,
                                       GhosttyRenderStateOption option,
                                       const void *value);
GhosttyResult ghostty_render_state_colors_get(GhosttyRenderState state,
                                              GhosttyRenderStateColors *out_colors);

GhosttyResult ghostty_render_state_row_iterator_new(const GhosttyAllocator *allocator,
                                                    GhosttyRenderStateRowIterator *out_iterator);
void ghostty_render_state_row_iterator_free(GhosttyRenderStateRowIterator iterator);
bool ghostty_render_state_row_iterator_next(GhosttyRenderStateRowIterator iterator);
GhosttyResult ghostty_render_state_row_get(GhosttyRenderStateRowIterator iterator,
                                           GhosttyRenderStateRowData data,
                                           void *out);
GhosttyResult ghostty_render_state_row_set(GhosttyRenderStateRowIterator iterator,
                                           GhosttyRenderStateRowOption option,
                                           const void *value);

GhosttyResult ghostty_render_state_row_cells_new(const GhosttyAllocator *allocator,
                                                 GhosttyRenderStateRowCells *out_cells);
void ghostty_render_state_row_cells_free(GhosttyRenderStateRowCells cells);
bool ghostty_render_state_row_cells_next(GhosttyRenderStateRowCells cells);
GhosttyResult ghostty_render_state_row_cells_get(GhosttyRenderStateRowCells cells,
                                                 GhosttyRenderStateRowCellsData data,
                                                 void *out);
