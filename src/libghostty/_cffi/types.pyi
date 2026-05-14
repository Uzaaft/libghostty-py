from collections.abc import Callable
from typing import Literal, Protocol, TypeAlias

GhosttyMode: TypeAlias = int
GhosttyMods: TypeAlias = int
GhosttyColorPaletteIndex: TypeAlias = int
GhosttyKittyKeyFlags: TypeAlias = int
GhosttySgrUnderline: TypeAlias = int
GhosttyMouseAction: TypeAlias = int
GhosttyMouseButton: TypeAlias = int
GhosttyRenderStateDirty: TypeAlias = int
GhosttyRenderStateCursorVisualStyle: TypeAlias = int
GhosttyStyleColorTag: TypeAlias = int

class GhosttyAllocator: ...
class GhosttyFormatter: ...
class GhosttyKeyEncoder: ...
class GhosttyKeyEvent: ...
class GhosttyKittyGraphics: ...
class GhosttyKittyGraphicsImage: ...
class GhosttyKittyGraphicsPlacementIterator: ...
class GhosttyMouseEncoder: ...
class GhosttyMouseEvent: ...
class GhosttyOscCommand: ...
class GhosttyOscParser: ...
class GhosttyRenderState: ...
class GhosttyRenderStateRowCells: ...
class GhosttyRenderStateRowIterator: ...
class GhosttySelection: ...
class GhosttySgrParser: ...
class GhosttyTerminal: ...

GhosttyResult: TypeAlias = Literal[0, -1, -2, -3, -4]
GhosttyBuildInfo: TypeAlias = Literal[1, 2, 3, 5, 6, 7, 8]
GhosttyTerminalScrollViewportTag: TypeAlias = Literal[0, 1, 2]
GhosttyTerminalScreen: TypeAlias = Literal[1]
GhosttyTerminalOption: TypeAlias = Literal[1, 6, 8, 11, 12, 15, 16, 17, 18, 19, 20]
GhosttyTerminalData: TypeAlias = Literal[1, 2, 3, 4, 6, 7, 12, 14, 15, 18, 19, 26, 27, 28, 29, 30]
GhosttySgrAttributeTag: TypeAlias = Literal[7, 8, 9, 21, 22, 23, 24, 27, 28, 29, 30]
GhosttyOscCommandType: TypeAlias = Literal[0, 1]
GhosttyOscCommandData: TypeAlias = Literal[1]
GhosttyKeyAction: TypeAlias = Literal[0, 1, 2]
GhosttyKeyEncoderOption: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 0x7FFFFFFF]
GhosttyKey: TypeAlias = Literal[
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
]
GhosttyKittyGraphicsData: TypeAlias = Literal[0, 1, 0x7FFFFFFF]
GhosttyKittyGraphicsPlacementData: TypeAlias = Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0x7FFFFFFF
]
GhosttyKittyPlacementLayer: TypeAlias = Literal[0, 1, 2, 3, 0x7FFFFFFF]
GhosttyKittyGraphicsPlacementIteratorOption: TypeAlias = Literal[0, 0x7FFFFFFF]
GhosttyKittyImageFormat: TypeAlias = Literal[0, 1, 2, 3, 4, 0x7FFFFFFF]
GhosttyKittyImageCompression: TypeAlias = Literal[0, 1, 0x7FFFFFFF]
GhosttyKittyGraphicsImageData: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 0x7FFFFFFF]
GhosttyFormatterFormat: TypeAlias = Literal[0, 1, 2]
GhosttyRenderStateData: TypeAlias = Literal[3, 4, 10, 11, 12, 14, 15, 16]
GhosttyRenderStateOption: TypeAlias = Literal[0]
GhosttyRenderStateRowData: TypeAlias = Literal[1, 3]
GhosttyRenderStateRowOption: TypeAlias = Literal[0]
GhosttyRenderStateRowCellsData: TypeAlias = Literal[2, 3, 4, 5, 6]

class GhosttyString:
    ptr: object
    len: int

class GhosttyColorRgb:
    r: int
    g: int
    b: int

class GhosttyTerminalOptions:
    cols: int
    rows: int
    max_scrollback: int

class GhosttyTerminalScrollViewportValue:
    delta: int
    _padding: list[int]

class GhosttyTerminalScrollViewport:
    tag: GhosttyTerminalScrollViewportTag
    value: GhosttyTerminalScrollViewportValue

class GhosttyDeviceAttributesPrimary:
    conformance_level: int
    features: list[int]
    num_features: int

class GhosttyDeviceAttributesSecondary:
    device_type: int
    firmware_version: int
    rom_cartridge: int

class GhosttyDeviceAttributesTertiary:
    unit_id: int

class GhosttyDeviceAttributes:
    primary: GhosttyDeviceAttributesPrimary
    secondary: GhosttyDeviceAttributesSecondary
    tertiary: GhosttyDeviceAttributesTertiary

class GhosttySizeReportSize:
    rows: int
    columns: int
    cell_width: int
    cell_height: int

class GhosttySgrAttributeValue:
    underline: GhosttySgrUnderline
    underline_color: GhosttyColorRgb
    underline_color_256: GhosttyColorPaletteIndex
    direct_color_fg: GhosttyColorRgb
    direct_color_bg: GhosttyColorRgb
    bg_8: GhosttyColorPaletteIndex
    fg_8: GhosttyColorPaletteIndex
    bright_bg_8: GhosttyColorPaletteIndex
    bright_fg_8: GhosttyColorPaletteIndex
    bg_256: GhosttyColorPaletteIndex
    fg_256: GhosttyColorPaletteIndex
    _padding: list[int]

class GhosttySgrAttribute:
    tag: GhosttySgrAttributeTag
    value: GhosttySgrAttributeValue

class GhosttyMousePosition:
    x: float
    y: float

class GhosttyKittyGraphicsPlacementRenderInfo:
    size: int
    pixel_width: int
    pixel_height: int
    grid_cols: int
    grid_rows: int
    viewport_col: int
    viewport_row: int
    viewport_visible: bool
    source_x: int
    source_y: int
    source_width: int
    source_height: int

class GhosttyFormatterScreenExtra:
    size: int
    cursor: bool
    style: bool
    hyperlink: bool
    protection: bool
    kitty_keyboard: bool
    charsets: bool

class GhosttyFormatterTerminalExtra:
    size: int
    palette: bool
    modes: bool
    scrolling_region: bool
    tabstops: bool
    pwd: bool
    keyboard: bool
    screen: GhosttyFormatterScreenExtra

class GhosttyFormatterTerminalOptions:
    size: int
    emit: GhosttyFormatterFormat
    unwrap: bool
    trim: bool
    extra: GhosttyFormatterTerminalExtra
    selection: object

class GhosttyStyleColorValue:
    palette: GhosttyColorPaletteIndex
    rgb: GhosttyColorRgb
    _padding: int

class GhosttyStyleColor:
    tag: GhosttyStyleColorTag
    value: GhosttyStyleColorValue

class GhosttyStyle:
    size: int
    fg_color: GhosttyStyleColor
    bg_color: GhosttyStyleColor
    underline_color: GhosttyStyleColor
    bold: bool
    italic: bool
    faint: bool
    blink: bool
    inverse: bool
    invisible: bool
    strikethrough: bool
    overline: bool
    underline: int

class GhosttyRenderStateColors:
    size: int
    background: GhosttyColorRgb
    foreground: GhosttyColorRgb
    cursor: GhosttyColorRgb
    cursor_has_value: bool
    palette: list[GhosttyColorRgb]

GhosttyTerminalWritePtyFn: TypeAlias = Callable[[GhosttyTerminal, object, object, int], None]
GhosttyTerminalSizeFn: TypeAlias = Callable[[GhosttyTerminal, object, object], bool]
GhosttyTerminalDeviceAttributesFn: TypeAlias = Callable[[GhosttyTerminal, object, object], bool]

def ghostty_free(allocator: object, ptr: object, length: int) -> None: ...
def ghostty_build_info(data: GhosttyBuildInfo, out: object) -> GhosttyResult: ...
def ghostty_terminal_new(
    allocator: object, terminal: object, options: GhosttyTerminalOptions
) -> GhosttyResult: ...
def ghostty_terminal_free(terminal: GhosttyTerminal) -> None: ...
def ghostty_terminal_reset(terminal: GhosttyTerminal) -> None: ...
def ghostty_terminal_resize(
    terminal: GhosttyTerminal, cols: int, rows: int, cell_width_px: int, cell_height_px: int
) -> GhosttyResult: ...
def ghostty_terminal_set(
    terminal: GhosttyTerminal, option: GhosttyTerminalOption, value: object
) -> GhosttyResult: ...
def ghostty_terminal_vt_write(terminal: GhosttyTerminal, data: object, length: int) -> None: ...
def ghostty_terminal_scroll_viewport(
    terminal: GhosttyTerminal, behavior: GhosttyTerminalScrollViewport
) -> None: ...
def ghostty_terminal_mode_get(
    terminal: GhosttyTerminal, mode: GhosttyMode, out_value: object
) -> GhosttyResult: ...
def ghostty_terminal_mode_set(
    terminal: GhosttyTerminal, mode: GhosttyMode, value: bool
) -> GhosttyResult: ...
def ghostty_terminal_get(
    terminal: GhosttyTerminal, data: GhosttyTerminalData, out: object
) -> GhosttyResult: ...
def ghostty_paste_is_safe(data: object, length: int) -> bool: ...
def ghostty_paste_encode(
    data: object, data_len: int, bracketed: bool, buf: object, buf_len: int, out_written: object
) -> GhosttyResult: ...
def ghostty_sgr_new(allocator: object, parser: object) -> GhosttyResult: ...
def ghostty_sgr_free(parser: GhosttySgrParser) -> None: ...
def ghostty_sgr_set_params(
    parser: GhosttySgrParser, params: object, separators: object, length: int
) -> GhosttyResult: ...
def ghostty_sgr_next(parser: GhosttySgrParser, attr: object) -> bool: ...
def ghostty_osc_new(allocator: object, parser: object) -> GhosttyResult: ...
def ghostty_osc_free(parser: GhosttyOscParser) -> None: ...
def ghostty_osc_reset(parser: GhosttyOscParser) -> None: ...
def ghostty_osc_next(parser: GhosttyOscParser, byte: int) -> None: ...
def ghostty_osc_end(parser: GhosttyOscParser, terminator: int) -> GhosttyOscCommand: ...
def ghostty_osc_command_type(command: GhosttyOscCommand) -> GhosttyOscCommandType: ...
def ghostty_osc_command_data(
    command: GhosttyOscCommand, data: GhosttyOscCommandData, out: object
) -> bool: ...
def ghostty_key_event_new(allocator: object, event: object) -> GhosttyResult: ...
def ghostty_key_event_free(event: GhosttyKeyEvent) -> None: ...
def ghostty_key_event_set_action(event: GhosttyKeyEvent, action: GhosttyKeyAction) -> None: ...
def ghostty_key_event_get_action(event: GhosttyKeyEvent) -> GhosttyKeyAction: ...
def ghostty_key_event_set_key(event: GhosttyKeyEvent, key: GhosttyKey) -> None: ...
def ghostty_key_event_get_key(event: GhosttyKeyEvent) -> GhosttyKey: ...
def ghostty_key_event_set_mods(event: GhosttyKeyEvent, mods: GhosttyMods) -> None: ...
def ghostty_key_event_get_mods(event: GhosttyKeyEvent) -> GhosttyMods: ...
def ghostty_key_event_set_consumed_mods(
    event: GhosttyKeyEvent, consumed_mods: GhosttyMods
) -> None: ...
def ghostty_key_event_get_consumed_mods(event: GhosttyKeyEvent) -> GhosttyMods: ...
def ghostty_key_event_set_composing(event: GhosttyKeyEvent, composing: bool) -> None: ...
def ghostty_key_event_get_composing(event: GhosttyKeyEvent) -> bool: ...
def ghostty_key_event_set_utf8(event: GhosttyKeyEvent, utf8: object, length: int) -> None: ...
def ghostty_key_event_get_utf8(event: GhosttyKeyEvent, length: object) -> object: ...
def ghostty_key_event_set_unshifted_codepoint(event: GhosttyKeyEvent, codepoint: int) -> None: ...
def ghostty_key_event_get_unshifted_codepoint(event: GhosttyKeyEvent) -> int: ...
def ghostty_key_encoder_new(allocator: object, encoder: object) -> GhosttyResult: ...
def ghostty_key_encoder_free(encoder: GhosttyKeyEncoder) -> None: ...
def ghostty_key_encoder_setopt_from_terminal(
    encoder: GhosttyKeyEncoder, terminal: GhosttyTerminal
) -> None: ...
def ghostty_key_encoder_setopt(
    encoder: GhosttyKeyEncoder, option: GhosttyKeyEncoderOption, value: object
) -> None: ...
def ghostty_key_encoder_encode(
    encoder: GhosttyKeyEncoder,
    event: GhosttyKeyEvent,
    out_buf: object,
    out_buf_size: int,
    out_len: object,
) -> GhosttyResult: ...
def ghostty_mouse_event_new(allocator: object, event: object) -> GhosttyResult: ...
def ghostty_mouse_event_free(event: GhosttyMouseEvent) -> None: ...
def ghostty_mouse_event_set_action(
    event: GhosttyMouseEvent, action: GhosttyMouseAction
) -> None: ...
def ghostty_mouse_event_get_action(event: GhosttyMouseEvent) -> GhosttyMouseAction: ...
def ghostty_mouse_event_set_button(
    event: GhosttyMouseEvent, button: GhosttyMouseButton
) -> None: ...
def ghostty_mouse_event_clear_button(event: GhosttyMouseEvent) -> None: ...
def ghostty_mouse_event_set_mods(event: GhosttyMouseEvent, mods: GhosttyMods) -> None: ...
def ghostty_mouse_event_get_mods(event: GhosttyMouseEvent) -> GhosttyMods: ...
def ghostty_mouse_event_set_position(
    event: GhosttyMouseEvent, position: GhosttyMousePosition
) -> None: ...
def ghostty_mouse_event_get_position(event: GhosttyMouseEvent) -> GhosttyMousePosition: ...
def ghostty_mouse_encoder_new(allocator: object, encoder: object) -> GhosttyResult: ...
def ghostty_mouse_encoder_free(encoder: GhosttyMouseEncoder) -> None: ...
def ghostty_mouse_encoder_setopt_from_terminal(
    encoder: GhosttyMouseEncoder, terminal: GhosttyTerminal
) -> None: ...
def ghostty_mouse_encoder_reset(encoder: GhosttyMouseEncoder) -> None: ...
def ghostty_mouse_encoder_encode(
    encoder: GhosttyMouseEncoder,
    event: GhosttyMouseEvent,
    out_buf: object,
    out_buf_size: int,
    out_len: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_get(
    graphics: GhosttyKittyGraphics, data: GhosttyKittyGraphicsData, out: object
) -> GhosttyResult: ...
def ghostty_kitty_graphics_image(
    graphics: GhosttyKittyGraphics, image_id: int
) -> GhosttyKittyGraphicsImage: ...
def ghostty_kitty_graphics_image_get(
    image: GhosttyKittyGraphicsImage, data: GhosttyKittyGraphicsImageData, out: object
) -> GhosttyResult: ...
def ghostty_kitty_graphics_image_get_multi(
    image: GhosttyKittyGraphicsImage, count: int, keys: object, values: object, out_written: object
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_iterator_new(
    allocator: object, out_iterator: object
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_iterator_free(
    iterator: GhosttyKittyGraphicsPlacementIterator,
) -> None: ...
def ghostty_kitty_graphics_placement_iterator_set(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    option: GhosttyKittyGraphicsPlacementIteratorOption,
    value: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_next(
    iterator: GhosttyKittyGraphicsPlacementIterator,
) -> bool: ...
def ghostty_kitty_graphics_placement_get(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    data: GhosttyKittyGraphicsPlacementData,
    out: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_get_multi(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    count: int,
    keys: object,
    values: object,
    out_written: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_rect(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_selection: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_pixel_size(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_width: object,
    out_height: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_grid_size(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_cols: object,
    out_rows: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_viewport_pos(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_col: object,
    out_row: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_source_rect(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    out_x: object,
    out_y: object,
    out_width: object,
    out_height: object,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_render_info(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_info: object,
) -> GhosttyResult: ...
def ghostty_formatter_terminal_new(
    allocator: object,
    formatter: object,
    terminal: GhosttyTerminal,
    options: GhosttyFormatterTerminalOptions,
) -> GhosttyResult: ...
def ghostty_formatter_format_alloc(
    formatter: GhosttyFormatter, allocator: object, out_ptr: object, out_len: object
) -> GhosttyResult: ...
def ghostty_formatter_free(formatter: GhosttyFormatter) -> None: ...
def ghostty_render_state_new(allocator: object, state: object) -> GhosttyResult: ...
def ghostty_render_state_free(state: GhosttyRenderState) -> None: ...
def ghostty_render_state_update(
    state: GhosttyRenderState, terminal: GhosttyTerminal
) -> GhosttyResult: ...
def ghostty_render_state_get(
    state: GhosttyRenderState, data: GhosttyRenderStateData, out: object
) -> GhosttyResult: ...
def ghostty_render_state_set(
    state: GhosttyRenderState, option: GhosttyRenderStateOption, value: object
) -> GhosttyResult: ...
def ghostty_render_state_colors_get(
    state: GhosttyRenderState, out_colors: object
) -> GhosttyResult: ...
def ghostty_render_state_row_iterator_new(
    allocator: object, out_iterator: object
) -> GhosttyResult: ...
def ghostty_render_state_row_iterator_free(iterator: GhosttyRenderStateRowIterator) -> None: ...
def ghostty_render_state_row_iterator_next(iterator: GhosttyRenderStateRowIterator) -> bool: ...
def ghostty_render_state_row_get(
    iterator: GhosttyRenderStateRowIterator, data: GhosttyRenderStateRowData, out: object
) -> GhosttyResult: ...
def ghostty_render_state_row_set(
    iterator: GhosttyRenderStateRowIterator, option: GhosttyRenderStateRowOption, value: object
) -> GhosttyResult: ...
def ghostty_render_state_row_cells_new(allocator: object, out_cells: object) -> GhosttyResult: ...
def ghostty_render_state_row_cells_free(cells: GhosttyRenderStateRowCells) -> None: ...
def ghostty_render_state_row_cells_next(cells: GhosttyRenderStateRowCells) -> bool: ...
def ghostty_render_state_row_cells_get(
    cells: GhosttyRenderStateRowCells, data: GhosttyRenderStateRowCellsData, out: object
) -> GhosttyResult: ...

class GhosttyVtLib(Protocol):
    GHOSTTY_SUCCESS: GhosttyResult
    GHOSTTY_OUT_OF_MEMORY: GhosttyResult
    GHOSTTY_INVALID_VALUE: GhosttyResult
    GHOSTTY_OUT_OF_SPACE: GhosttyResult
    GHOSTTY_NO_VALUE: GhosttyResult
    GHOSTTY_BUILD_INFO_SIMD: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_KITTY_GRAPHICS: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_TMUX_CONTROL_MODE: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_VERSION_STRING: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_VERSION_MAJOR: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_VERSION_MINOR: GhosttyBuildInfo
    GHOSTTY_BUILD_INFO_VERSION_PATCH: GhosttyBuildInfo
    GHOSTTY_SCROLL_VIEWPORT_TOP: GhosttyTerminalScrollViewportTag
    GHOSTTY_SCROLL_VIEWPORT_BOTTOM: GhosttyTerminalScrollViewportTag
    GHOSTTY_SCROLL_VIEWPORT_DELTA: GhosttyTerminalScrollViewportTag
    GHOSTTY_TERMINAL_SCREEN_ALTERNATE: GhosttyTerminalScreen
    GHOSTTY_TERMINAL_OPT_WRITE_PTY: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_SIZE: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_DEVICE_ATTRIBUTES: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_COLOR_FOREGROUND: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_COLOR_BACKGROUND: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_STORAGE_LIMIT: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_FILE: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_TEMP_FILE: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_SHARED_MEM: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_APC_MAX_BYTES: GhosttyTerminalOption
    GHOSTTY_TERMINAL_OPT_APC_MAX_BYTES_KITTY: GhosttyTerminalOption
    GHOSTTY_TERMINAL_DATA_COLS: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_ROWS: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_CURSOR_X: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_CURSOR_Y: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_ACTIVE_SCREEN: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_CURSOR_VISIBLE: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_TITLE: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_TOTAL_ROWS: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_SCROLLBACK_ROWS: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_COLOR_FOREGROUND: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_COLOR_BACKGROUND: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_STORAGE_LIMIT: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_FILE: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_TEMP_FILE: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_SHARED_MEM: GhosttyTerminalData
    GHOSTTY_TERMINAL_DATA_KITTY_GRAPHICS: GhosttyTerminalData
    GHOSTTY_SGR_ATTR_UNDERLINE: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_UNDERLINE_COLOR: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_UNDERLINE_COLOR_256: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_DIRECT_COLOR_FG: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_DIRECT_COLOR_BG: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_BG_8: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_FG_8: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_BRIGHT_BG_8: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_BRIGHT_FG_8: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_BG_256: GhosttySgrAttributeTag
    GHOSTTY_SGR_ATTR_FG_256: GhosttySgrAttributeTag
    GHOSTTY_OSC_COMMAND_INVALID: GhosttyOscCommandType
    GHOSTTY_OSC_COMMAND_CHANGE_WINDOW_TITLE: GhosttyOscCommandType
    GHOSTTY_OSC_DATA_CHANGE_WINDOW_TITLE_STR: GhosttyOscCommandData
    GHOSTTY_KEY_ACTION_RELEASE: GhosttyKeyAction
    GHOSTTY_KEY_ACTION_PRESS: GhosttyKeyAction
    GHOSTTY_KEY_ACTION_REPEAT: GhosttyKeyAction
    GHOSTTY_KEY_ENCODER_OPT_CURSOR_KEY_APPLICATION: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_KEYPAD_KEY_APPLICATION: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_IGNORE_KEYPAD_WITH_NUMLOCK: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_ALT_ESC_PREFIX: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_MODIFY_OTHER_KEYS_STATE_2: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_KITTY_FLAGS: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_MACOS_OPTION_AS_ALT: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_BACKARROW_KEY_MODE: GhosttyKeyEncoderOption
    GHOSTTY_KEY_ENCODER_OPT_MAX_VALUE: GhosttyKeyEncoderOption
    GHOSTTY_KEY_UNIDENTIFIED: GhosttyKey
    GHOSTTY_KEY_BACKQUOTE: GhosttyKey
    GHOSTTY_KEY_BACKSLASH: GhosttyKey
    GHOSTTY_KEY_BRACKET_LEFT: GhosttyKey
    GHOSTTY_KEY_BRACKET_RIGHT: GhosttyKey
    GHOSTTY_KEY_COMMA: GhosttyKey
    GHOSTTY_KEY_DIGIT_0: GhosttyKey
    GHOSTTY_KEY_DIGIT_1: GhosttyKey
    GHOSTTY_KEY_DIGIT_2: GhosttyKey
    GHOSTTY_KEY_DIGIT_3: GhosttyKey
    GHOSTTY_KEY_DIGIT_4: GhosttyKey
    GHOSTTY_KEY_DIGIT_5: GhosttyKey
    GHOSTTY_KEY_DIGIT_6: GhosttyKey
    GHOSTTY_KEY_DIGIT_7: GhosttyKey
    GHOSTTY_KEY_DIGIT_8: GhosttyKey
    GHOSTTY_KEY_DIGIT_9: GhosttyKey
    GHOSTTY_KEY_EQUAL: GhosttyKey
    GHOSTTY_KEY_INTL_BACKSLASH: GhosttyKey
    GHOSTTY_KEY_INTL_RO: GhosttyKey
    GHOSTTY_KEY_INTL_YEN: GhosttyKey
    GHOSTTY_KEY_A: GhosttyKey
    GHOSTTY_KEY_B: GhosttyKey
    GHOSTTY_KEY_C: GhosttyKey
    GHOSTTY_KEY_D: GhosttyKey
    GHOSTTY_KEY_E: GhosttyKey
    GHOSTTY_KEY_F: GhosttyKey
    GHOSTTY_KEY_G: GhosttyKey
    GHOSTTY_KEY_H: GhosttyKey
    GHOSTTY_KEY_I: GhosttyKey
    GHOSTTY_KEY_J: GhosttyKey
    GHOSTTY_KEY_K: GhosttyKey
    GHOSTTY_KEY_L: GhosttyKey
    GHOSTTY_KEY_M: GhosttyKey
    GHOSTTY_KEY_N: GhosttyKey
    GHOSTTY_KEY_O: GhosttyKey
    GHOSTTY_KEY_P: GhosttyKey
    GHOSTTY_KEY_Q: GhosttyKey
    GHOSTTY_KEY_R: GhosttyKey
    GHOSTTY_KEY_S: GhosttyKey
    GHOSTTY_KEY_T: GhosttyKey
    GHOSTTY_KEY_U: GhosttyKey
    GHOSTTY_KEY_V: GhosttyKey
    GHOSTTY_KEY_W: GhosttyKey
    GHOSTTY_KEY_X: GhosttyKey
    GHOSTTY_KEY_Y: GhosttyKey
    GHOSTTY_KEY_Z: GhosttyKey
    GHOSTTY_KEY_MINUS: GhosttyKey
    GHOSTTY_KEY_PERIOD: GhosttyKey
    GHOSTTY_KEY_QUOTE: GhosttyKey
    GHOSTTY_KEY_SEMICOLON: GhosttyKey
    GHOSTTY_KEY_SLASH: GhosttyKey
    GHOSTTY_KEY_ALT_LEFT: GhosttyKey
    GHOSTTY_KEY_ALT_RIGHT: GhosttyKey
    GHOSTTY_KEY_BACKSPACE: GhosttyKey
    GHOSTTY_KEY_CAPS_LOCK: GhosttyKey
    GHOSTTY_KEY_CONTEXT_MENU: GhosttyKey
    GHOSTTY_KEY_CONTROL_LEFT: GhosttyKey
    GHOSTTY_KEY_CONTROL_RIGHT: GhosttyKey
    GHOSTTY_KEY_ENTER: GhosttyKey
    GHOSTTY_KEY_META_LEFT: GhosttyKey
    GHOSTTY_KEY_META_RIGHT: GhosttyKey
    GHOSTTY_KEY_SHIFT_LEFT: GhosttyKey
    GHOSTTY_KEY_SHIFT_RIGHT: GhosttyKey
    GHOSTTY_KEY_SPACE: GhosttyKey
    GHOSTTY_KEY_TAB: GhosttyKey
    GHOSTTY_KEY_CONVERT: GhosttyKey
    GHOSTTY_KEY_KANA_MODE: GhosttyKey
    GHOSTTY_KEY_NON_CONVERT: GhosttyKey
    GHOSTTY_KEY_DELETE: GhosttyKey
    GHOSTTY_KEY_END: GhosttyKey
    GHOSTTY_KEY_HELP: GhosttyKey
    GHOSTTY_KEY_HOME: GhosttyKey
    GHOSTTY_KEY_INSERT: GhosttyKey
    GHOSTTY_KEY_PAGE_DOWN: GhosttyKey
    GHOSTTY_KEY_PAGE_UP: GhosttyKey
    GHOSTTY_KEY_ARROW_DOWN: GhosttyKey
    GHOSTTY_KEY_ARROW_LEFT: GhosttyKey
    GHOSTTY_KEY_ARROW_RIGHT: GhosttyKey
    GHOSTTY_KEY_ARROW_UP: GhosttyKey
    GHOSTTY_KEY_NUM_LOCK: GhosttyKey
    GHOSTTY_KEY_NUMPAD_0: GhosttyKey
    GHOSTTY_KEY_NUMPAD_1: GhosttyKey
    GHOSTTY_KEY_NUMPAD_2: GhosttyKey
    GHOSTTY_KEY_NUMPAD_3: GhosttyKey
    GHOSTTY_KEY_NUMPAD_4: GhosttyKey
    GHOSTTY_KEY_NUMPAD_5: GhosttyKey
    GHOSTTY_KEY_NUMPAD_6: GhosttyKey
    GHOSTTY_KEY_NUMPAD_7: GhosttyKey
    GHOSTTY_KEY_NUMPAD_8: GhosttyKey
    GHOSTTY_KEY_NUMPAD_9: GhosttyKey
    GHOSTTY_KEY_NUMPAD_ADD: GhosttyKey
    GHOSTTY_KEY_NUMPAD_BACKSPACE: GhosttyKey
    GHOSTTY_KEY_NUMPAD_CLEAR: GhosttyKey
    GHOSTTY_KEY_NUMPAD_CLEAR_ENTRY: GhosttyKey
    GHOSTTY_KEY_NUMPAD_COMMA: GhosttyKey
    GHOSTTY_KEY_NUMPAD_DECIMAL: GhosttyKey
    GHOSTTY_KEY_NUMPAD_DIVIDE: GhosttyKey
    GHOSTTY_KEY_NUMPAD_ENTER: GhosttyKey
    GHOSTTY_KEY_NUMPAD_EQUAL: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MEMORY_ADD: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MEMORY_CLEAR: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MEMORY_RECALL: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MEMORY_STORE: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MEMORY_SUBTRACT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_MULTIPLY: GhosttyKey
    GHOSTTY_KEY_NUMPAD_PAREN_LEFT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_PAREN_RIGHT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_SUBTRACT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_SEPARATOR: GhosttyKey
    GHOSTTY_KEY_NUMPAD_UP: GhosttyKey
    GHOSTTY_KEY_NUMPAD_DOWN: GhosttyKey
    GHOSTTY_KEY_NUMPAD_RIGHT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_LEFT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_BEGIN: GhosttyKey
    GHOSTTY_KEY_NUMPAD_HOME: GhosttyKey
    GHOSTTY_KEY_NUMPAD_END: GhosttyKey
    GHOSTTY_KEY_NUMPAD_INSERT: GhosttyKey
    GHOSTTY_KEY_NUMPAD_DELETE: GhosttyKey
    GHOSTTY_KEY_NUMPAD_PAGE_UP: GhosttyKey
    GHOSTTY_KEY_NUMPAD_PAGE_DOWN: GhosttyKey
    GHOSTTY_KEY_ESCAPE: GhosttyKey
    GHOSTTY_KEY_F1: GhosttyKey
    GHOSTTY_KEY_F2: GhosttyKey
    GHOSTTY_KEY_F3: GhosttyKey
    GHOSTTY_KEY_F4: GhosttyKey
    GHOSTTY_KEY_F5: GhosttyKey
    GHOSTTY_KEY_F6: GhosttyKey
    GHOSTTY_KEY_F7: GhosttyKey
    GHOSTTY_KEY_F8: GhosttyKey
    GHOSTTY_KEY_F9: GhosttyKey
    GHOSTTY_KEY_F10: GhosttyKey
    GHOSTTY_KEY_F11: GhosttyKey
    GHOSTTY_KEY_F12: GhosttyKey
    GHOSTTY_KITTY_GRAPHICS_DATA_INVALID: GhosttyKittyGraphicsData
    GHOSTTY_KITTY_GRAPHICS_DATA_PLACEMENT_ITERATOR: GhosttyKittyGraphicsData
    GHOSTTY_KITTY_GRAPHICS_DATA_MAX_VALUE: GhosttyKittyGraphicsData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_INVALID: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_IMAGE_ID: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_PLACEMENT_ID: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_IS_VIRTUAL: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_X_OFFSET: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_Y_OFFSET: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_X: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_Y: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_WIDTH: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_SOURCE_HEIGHT: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_COLUMNS: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_ROWS: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_Z: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_DATA_MAX_VALUE: GhosttyKittyGraphicsPlacementData
    GHOSTTY_KITTY_PLACEMENT_LAYER_ALL: GhosttyKittyPlacementLayer
    GHOSTTY_KITTY_PLACEMENT_LAYER_BELOW_BG: GhosttyKittyPlacementLayer
    GHOSTTY_KITTY_PLACEMENT_LAYER_BELOW_TEXT: GhosttyKittyPlacementLayer
    GHOSTTY_KITTY_PLACEMENT_LAYER_ABOVE_TEXT: GhosttyKittyPlacementLayer
    GHOSTTY_KITTY_PLACEMENT_LAYER_MAX_VALUE: GhosttyKittyPlacementLayer
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_ITERATOR_OPTION_LAYER: (
        GhosttyKittyGraphicsPlacementIteratorOption
    )
    GHOSTTY_KITTY_GRAPHICS_PLACEMENT_ITERATOR_OPTION_MAX_VALUE: (
        GhosttyKittyGraphicsPlacementIteratorOption
    )
    GHOSTTY_KITTY_IMAGE_FORMAT_RGB: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_FORMAT_RGBA: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_FORMAT_PNG: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_FORMAT_GRAY_ALPHA: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_FORMAT_GRAY: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_FORMAT_MAX_VALUE: GhosttyKittyImageFormat
    GHOSTTY_KITTY_IMAGE_COMPRESSION_NONE: GhosttyKittyImageCompression
    GHOSTTY_KITTY_IMAGE_COMPRESSION_ZLIB_DEFLATE: GhosttyKittyImageCompression
    GHOSTTY_KITTY_IMAGE_COMPRESSION_MAX_VALUE: GhosttyKittyImageCompression
    GHOSTTY_KITTY_IMAGE_DATA_INVALID: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_ID: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_NUMBER: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_WIDTH: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_HEIGHT: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_FORMAT: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_COMPRESSION: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_DATA_PTR: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_DATA_LEN: GhosttyKittyGraphicsImageData
    GHOSTTY_KITTY_IMAGE_DATA_MAX_VALUE: GhosttyKittyGraphicsImageData
    GHOSTTY_FORMATTER_FORMAT_PLAIN: GhosttyFormatterFormat
    GHOSTTY_FORMATTER_FORMAT_VT: GhosttyFormatterFormat
    GHOSTTY_FORMATTER_FORMAT_HTML: GhosttyFormatterFormat
    GHOSTTY_RENDER_STATE_DATA_DIRTY: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_ROW_ITERATOR: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VISUAL_STYLE: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VISIBLE: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_BLINKING: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_HAS_VALUE: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_X: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_Y: GhosttyRenderStateData
    GHOSTTY_RENDER_STATE_OPTION_DIRTY: GhosttyRenderStateOption
    GHOSTTY_RENDER_STATE_ROW_DATA_DIRTY: GhosttyRenderStateRowData
    GHOSTTY_RENDER_STATE_ROW_DATA_CELLS: GhosttyRenderStateRowData
    GHOSTTY_RENDER_STATE_ROW_OPTION_DIRTY: GhosttyRenderStateRowOption
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_STYLE: GhosttyRenderStateRowCellsData
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_LEN: GhosttyRenderStateRowCellsData
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_BUF: GhosttyRenderStateRowCellsData
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_BG_COLOR: GhosttyRenderStateRowCellsData
    GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_FG_COLOR: GhosttyRenderStateRowCellsData

    def ghostty_free(self, allocator: object, ptr: object, length: int) -> None: ...
    def ghostty_build_info(self, data: GhosttyBuildInfo, out: object) -> GhosttyResult: ...
    def ghostty_terminal_new(
        self, allocator: object, terminal: object, options: GhosttyTerminalOptions
    ) -> GhosttyResult: ...
    def ghostty_terminal_free(self, terminal: GhosttyTerminal) -> None: ...
    def ghostty_terminal_reset(self, terminal: GhosttyTerminal) -> None: ...
    def ghostty_terminal_resize(
        self,
        terminal: GhosttyTerminal,
        cols: int,
        rows: int,
        cell_width_px: int,
        cell_height_px: int,
    ) -> GhosttyResult: ...
    def ghostty_terminal_set(
        self, terminal: GhosttyTerminal, option: GhosttyTerminalOption, value: object
    ) -> GhosttyResult: ...
    def ghostty_terminal_vt_write(
        self, terminal: GhosttyTerminal, data: object, length: int
    ) -> None: ...
    def ghostty_terminal_scroll_viewport(
        self, terminal: GhosttyTerminal, behavior: GhosttyTerminalScrollViewport
    ) -> None: ...
    def ghostty_terminal_mode_get(
        self, terminal: GhosttyTerminal, mode: GhosttyMode, out_value: object
    ) -> GhosttyResult: ...
    def ghostty_terminal_mode_set(
        self, terminal: GhosttyTerminal, mode: GhosttyMode, value: bool
    ) -> GhosttyResult: ...
    def ghostty_terminal_get(
        self, terminal: GhosttyTerminal, data: GhosttyTerminalData, out: object
    ) -> GhosttyResult: ...
    def ghostty_paste_is_safe(self, data: object, length: int) -> bool: ...
    def ghostty_paste_encode(
        self,
        data: object,
        data_len: int,
        bracketed: bool,
        buf: object,
        buf_len: int,
        out_written: object,
    ) -> GhosttyResult: ...
    def ghostty_sgr_new(self, allocator: object, parser: object) -> GhosttyResult: ...
    def ghostty_sgr_free(self, parser: GhosttySgrParser) -> None: ...
    def ghostty_sgr_set_params(
        self, parser: GhosttySgrParser, params: object, separators: object, length: int
    ) -> GhosttyResult: ...
    def ghostty_sgr_next(self, parser: GhosttySgrParser, attr: object) -> bool: ...
    def ghostty_osc_new(self, allocator: object, parser: object) -> GhosttyResult: ...
    def ghostty_osc_free(self, parser: GhosttyOscParser) -> None: ...
    def ghostty_osc_reset(self, parser: GhosttyOscParser) -> None: ...
    def ghostty_osc_next(self, parser: GhosttyOscParser, byte: int) -> None: ...
    def ghostty_osc_end(self, parser: GhosttyOscParser, terminator: int) -> GhosttyOscCommand: ...
    def ghostty_osc_command_type(self, command: GhosttyOscCommand) -> GhosttyOscCommandType: ...
    def ghostty_osc_command_data(
        self, command: GhosttyOscCommand, data: GhosttyOscCommandData, out: object
    ) -> bool: ...
    def ghostty_key_event_new(self, allocator: object, event: object) -> GhosttyResult: ...
    def ghostty_key_event_free(self, event: GhosttyKeyEvent) -> None: ...
    def ghostty_key_event_set_action(
        self, event: GhosttyKeyEvent, action: GhosttyKeyAction
    ) -> None: ...
    def ghostty_key_event_get_action(self, event: GhosttyKeyEvent) -> GhosttyKeyAction: ...
    def ghostty_key_event_set_key(self, event: GhosttyKeyEvent, key: GhosttyKey) -> None: ...
    def ghostty_key_event_get_key(self, event: GhosttyKeyEvent) -> GhosttyKey: ...
    def ghostty_key_event_set_mods(self, event: GhosttyKeyEvent, mods: GhosttyMods) -> None: ...
    def ghostty_key_event_get_mods(self, event: GhosttyKeyEvent) -> GhosttyMods: ...
    def ghostty_key_event_set_consumed_mods(
        self, event: GhosttyKeyEvent, consumed_mods: GhosttyMods
    ) -> None: ...
    def ghostty_key_event_get_consumed_mods(self, event: GhosttyKeyEvent) -> GhosttyMods: ...
    def ghostty_key_event_set_composing(self, event: GhosttyKeyEvent, composing: bool) -> None: ...
    def ghostty_key_event_get_composing(self, event: GhosttyKeyEvent) -> bool: ...
    def ghostty_key_event_set_utf8(
        self, event: GhosttyKeyEvent, utf8: object, length: int
    ) -> None: ...
    def ghostty_key_event_get_utf8(self, event: GhosttyKeyEvent, length: object) -> object: ...
    def ghostty_key_event_set_unshifted_codepoint(
        self, event: GhosttyKeyEvent, codepoint: int
    ) -> None: ...
    def ghostty_key_event_get_unshifted_codepoint(self, event: GhosttyKeyEvent) -> int: ...
    def ghostty_key_encoder_new(self, allocator: object, encoder: object) -> GhosttyResult: ...
    def ghostty_key_encoder_free(self, encoder: GhosttyKeyEncoder) -> None: ...
    def ghostty_key_encoder_setopt_from_terminal(
        self, encoder: GhosttyKeyEncoder, terminal: GhosttyTerminal
    ) -> None: ...
    def ghostty_key_encoder_setopt(
        self, encoder: GhosttyKeyEncoder, option: GhosttyKeyEncoderOption, value: object
    ) -> None: ...
    def ghostty_key_encoder_encode(
        self,
        encoder: GhosttyKeyEncoder,
        event: GhosttyKeyEvent,
        out_buf: object,
        out_buf_size: int,
        out_len: object,
    ) -> GhosttyResult: ...
    def ghostty_mouse_event_new(self, allocator: object, event: object) -> GhosttyResult: ...
    def ghostty_mouse_event_free(self, event: GhosttyMouseEvent) -> None: ...
    def ghostty_mouse_event_set_action(
        self, event: GhosttyMouseEvent, action: GhosttyMouseAction
    ) -> None: ...
    def ghostty_mouse_event_get_action(self, event: GhosttyMouseEvent) -> GhosttyMouseAction: ...
    def ghostty_mouse_event_set_button(
        self, event: GhosttyMouseEvent, button: GhosttyMouseButton
    ) -> None: ...
    def ghostty_mouse_event_clear_button(self, event: GhosttyMouseEvent) -> None: ...
    def ghostty_mouse_event_set_mods(self, event: GhosttyMouseEvent, mods: GhosttyMods) -> None: ...
    def ghostty_mouse_event_get_mods(self, event: GhosttyMouseEvent) -> GhosttyMods: ...
    def ghostty_mouse_event_set_position(
        self, event: GhosttyMouseEvent, position: GhosttyMousePosition
    ) -> None: ...
    def ghostty_mouse_event_get_position(
        self, event: GhosttyMouseEvent
    ) -> GhosttyMousePosition: ...
    def ghostty_mouse_encoder_new(self, allocator: object, encoder: object) -> GhosttyResult: ...
    def ghostty_mouse_encoder_free(self, encoder: GhosttyMouseEncoder) -> None: ...
    def ghostty_mouse_encoder_setopt_from_terminal(
        self, encoder: GhosttyMouseEncoder, terminal: GhosttyTerminal
    ) -> None: ...
    def ghostty_mouse_encoder_reset(self, encoder: GhosttyMouseEncoder) -> None: ...
    def ghostty_mouse_encoder_encode(
        self,
        encoder: GhosttyMouseEncoder,
        event: GhosttyMouseEvent,
        out_buf: object,
        out_buf_size: int,
        out_len: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_get(
        self, graphics: GhosttyKittyGraphics, data: GhosttyKittyGraphicsData, out: object
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_image(
        self, graphics: GhosttyKittyGraphics, image_id: int
    ) -> GhosttyKittyGraphicsImage: ...
    def ghostty_kitty_graphics_image_get(
        self, image: GhosttyKittyGraphicsImage, data: GhosttyKittyGraphicsImageData, out: object
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_image_get_multi(
        self,
        image: GhosttyKittyGraphicsImage,
        count: int,
        keys: object,
        values: object,
        out_written: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_iterator_new(
        self, allocator: object, out_iterator: object
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_iterator_free(
        self, iterator: GhosttyKittyGraphicsPlacementIterator
    ) -> None: ...
    def ghostty_kitty_graphics_placement_iterator_set(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        option: GhosttyKittyGraphicsPlacementIteratorOption,
        value: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_next(
        self, iterator: GhosttyKittyGraphicsPlacementIterator
    ) -> bool: ...
    def ghostty_kitty_graphics_placement_get(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        data: GhosttyKittyGraphicsPlacementData,
        out: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_get_multi(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        count: int,
        keys: object,
        values: object,
        out_written: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_rect(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        terminal: GhosttyTerminal,
        out_selection: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_pixel_size(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        terminal: GhosttyTerminal,
        out_width: object,
        out_height: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_grid_size(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        terminal: GhosttyTerminal,
        out_cols: object,
        out_rows: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_viewport_pos(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        terminal: GhosttyTerminal,
        out_col: object,
        out_row: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_source_rect(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        out_x: object,
        out_y: object,
        out_width: object,
        out_height: object,
    ) -> GhosttyResult: ...
    def ghostty_kitty_graphics_placement_render_info(
        self,
        iterator: GhosttyKittyGraphicsPlacementIterator,
        image: GhosttyKittyGraphicsImage,
        terminal: GhosttyTerminal,
        out_info: object,
    ) -> GhosttyResult: ...
    def ghostty_formatter_terminal_new(
        self,
        allocator: object,
        formatter: object,
        terminal: GhosttyTerminal,
        options: GhosttyFormatterTerminalOptions,
    ) -> GhosttyResult: ...
    def ghostty_formatter_format_alloc(
        self, formatter: GhosttyFormatter, allocator: object, out_ptr: object, out_len: object
    ) -> GhosttyResult: ...
    def ghostty_formatter_free(self, formatter: GhosttyFormatter) -> None: ...
    def ghostty_render_state_new(self, allocator: object, state: object) -> GhosttyResult: ...
    def ghostty_render_state_free(self, state: GhosttyRenderState) -> None: ...
    def ghostty_render_state_update(
        self, state: GhosttyRenderState, terminal: GhosttyTerminal
    ) -> GhosttyResult: ...
    def ghostty_render_state_get(
        self, state: GhosttyRenderState, data: GhosttyRenderStateData, out: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_set(
        self, state: GhosttyRenderState, option: GhosttyRenderStateOption, value: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_colors_get(
        self, state: GhosttyRenderState, out_colors: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_row_iterator_new(
        self, allocator: object, out_iterator: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_row_iterator_free(
        self, iterator: GhosttyRenderStateRowIterator
    ) -> None: ...
    def ghostty_render_state_row_iterator_next(
        self, iterator: GhosttyRenderStateRowIterator
    ) -> bool: ...
    def ghostty_render_state_row_get(
        self, iterator: GhosttyRenderStateRowIterator, data: GhosttyRenderStateRowData, out: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_row_set(
        self,
        iterator: GhosttyRenderStateRowIterator,
        option: GhosttyRenderStateRowOption,
        value: object,
    ) -> GhosttyResult: ...
    def ghostty_render_state_row_cells_new(
        self, allocator: object, out_cells: object
    ) -> GhosttyResult: ...
    def ghostty_render_state_row_cells_free(self, cells: GhosttyRenderStateRowCells) -> None: ...
    def ghostty_render_state_row_cells_next(self, cells: GhosttyRenderStateRowCells) -> bool: ...
    def ghostty_render_state_row_cells_get(
        self, cells: GhosttyRenderStateRowCells, data: GhosttyRenderStateRowCellsData, out: object
    ) -> GhosttyResult: ...
