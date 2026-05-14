from collections.abc import Callable
from typing import Literal, TypeAlias

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
    ptr: int
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
    selection: GhosttySelection


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


GhosttyTerminalWritePtyFn: TypeAlias = Callable[[GhosttyTerminal, object, int, int], None]
GhosttyTerminalSizeFn: TypeAlias = Callable[[GhosttyTerminal, object, GhosttySizeReportSize], bool]
GhosttyTerminalDeviceAttributesFn: TypeAlias = Callable[
    [GhosttyTerminal, object, GhosttyDeviceAttributes], bool
]


def ghostty_free(allocator: GhosttyAllocator, ptr: int, len: int) -> None: ...
def ghostty_build_info(data: GhosttyBuildInfo, out: object) -> GhosttyResult: ...
def ghostty_terminal_new(
    allocator: GhosttyAllocator, terminal: GhosttyTerminal, options: GhosttyTerminalOptions
) -> GhosttyResult: ...
def ghostty_terminal_free(terminal: GhosttyTerminal) -> None: ...
def ghostty_terminal_reset(terminal: GhosttyTerminal) -> None: ...
def ghostty_terminal_resize(
    terminal: GhosttyTerminal, cols: int, rows: int, cell_width_px: int, cell_height_px: int
) -> GhosttyResult: ...
def ghostty_terminal_set(
    terminal: GhosttyTerminal, option: GhosttyTerminalOption, value: object
) -> GhosttyResult: ...
def ghostty_terminal_vt_write(terminal: GhosttyTerminal, data: int, len: int) -> None: ...
def ghostty_terminal_scroll_viewport(
    terminal: GhosttyTerminal, behavior: GhosttyTerminalScrollViewport
) -> None: ...
def ghostty_terminal_mode_get(
    terminal: GhosttyTerminal, mode: GhosttyMode, out_value: bool
) -> GhosttyResult: ...
def ghostty_terminal_mode_set(
    terminal: GhosttyTerminal, mode: GhosttyMode, value: bool
) -> GhosttyResult: ...
def ghostty_terminal_get(
    terminal: GhosttyTerminal, data: GhosttyTerminalData, out: object
) -> GhosttyResult: ...
def ghostty_paste_is_safe(data: str, len: int) -> bool: ...
def ghostty_paste_encode(
    data: str, data_len: int, bracketed: bool, buf: str, buf_len: int, out_written: int
) -> GhosttyResult: ...
def ghostty_sgr_new(allocator: GhosttyAllocator, parser: GhosttySgrParser) -> GhosttyResult: ...
def ghostty_sgr_free(parser: GhosttySgrParser) -> None: ...
def ghostty_sgr_set_params(
    parser: GhosttySgrParser, params: int, separators: str, len: int
) -> GhosttyResult: ...
def ghostty_sgr_next(parser: GhosttySgrParser, attr: GhosttySgrAttribute) -> bool: ...
def ghostty_osc_new(allocator: GhosttyAllocator, parser: GhosttyOscParser) -> GhosttyResult: ...
def ghostty_osc_free(parser: GhosttyOscParser) -> None: ...
def ghostty_osc_reset(parser: GhosttyOscParser) -> None: ...
def ghostty_osc_next(parser: GhosttyOscParser, byte: int) -> None: ...
def ghostty_osc_end(parser: GhosttyOscParser, terminator: int) -> GhosttyOscCommand: ...
def ghostty_osc_command_type(command: GhosttyOscCommand) -> GhosttyOscCommandType: ...
def ghostty_osc_command_data(
    command: GhosttyOscCommand, data: GhosttyOscCommandData, out: object
) -> bool: ...
def ghostty_key_event_new(allocator: GhosttyAllocator, event: GhosttyKeyEvent) -> GhosttyResult: ...
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
def ghostty_key_event_set_utf8(event: GhosttyKeyEvent, utf8: str, len: int) -> None: ...
def ghostty_key_event_set_unshifted_codepoint(event: GhosttyKeyEvent, codepoint: int) -> None: ...
def ghostty_key_event_get_unshifted_codepoint(event: GhosttyKeyEvent) -> int: ...
def ghostty_key_encoder_new(
    allocator: GhosttyAllocator, encoder: GhosttyKeyEncoder
) -> GhosttyResult: ...
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
    out_buf: str,
    out_buf_size: int,
    out_len: int,
) -> GhosttyResult: ...
def ghostty_mouse_event_new(
    allocator: GhosttyAllocator, event: GhosttyMouseEvent
) -> GhosttyResult: ...
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
def ghostty_mouse_encoder_new(
    allocator: GhosttyAllocator, encoder: GhosttyMouseEncoder
) -> GhosttyResult: ...
def ghostty_mouse_encoder_free(encoder: GhosttyMouseEncoder) -> None: ...
def ghostty_mouse_encoder_setopt_from_terminal(
    encoder: GhosttyMouseEncoder, terminal: GhosttyTerminal
) -> None: ...
def ghostty_mouse_encoder_reset(encoder: GhosttyMouseEncoder) -> None: ...
def ghostty_mouse_encoder_encode(
    encoder: GhosttyMouseEncoder,
    event: GhosttyMouseEvent,
    out_buf: str,
    out_buf_size: int,
    out_len: int,
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
    image: GhosttyKittyGraphicsImage,
    count: int,
    keys: GhosttyKittyGraphicsImageData,
    values: None,
    out_written: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_iterator_new(
    allocator: GhosttyAllocator, out_iterator: GhosttyKittyGraphicsPlacementIterator
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
    keys: GhosttyKittyGraphicsPlacementData,
    values: None,
    out_written: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_rect(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_selection: GhosttySelection,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_pixel_size(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_width: int,
    out_height: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_grid_size(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_cols: int,
    out_rows: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_viewport_pos(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_col: int,
    out_row: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_source_rect(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    out_x: int,
    out_y: int,
    out_width: int,
    out_height: int,
) -> GhosttyResult: ...
def ghostty_kitty_graphics_placement_render_info(
    iterator: GhosttyKittyGraphicsPlacementIterator,
    image: GhosttyKittyGraphicsImage,
    terminal: GhosttyTerminal,
    out_info: GhosttyKittyGraphicsPlacementRenderInfo,
) -> GhosttyResult: ...
def ghostty_formatter_terminal_new(
    allocator: GhosttyAllocator,
    formatter: GhosttyFormatter,
    terminal: GhosttyTerminal,
    options: GhosttyFormatterTerminalOptions,
) -> GhosttyResult: ...
def ghostty_formatter_format_alloc(
    formatter: GhosttyFormatter, allocator: GhosttyAllocator, out_ptr: int, out_len: int
) -> GhosttyResult: ...
def ghostty_formatter_free(formatter: GhosttyFormatter) -> None: ...
def ghostty_render_state_new(
    allocator: GhosttyAllocator, state: GhosttyRenderState
) -> GhosttyResult: ...
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
    state: GhosttyRenderState, out_colors: GhosttyRenderStateColors
) -> GhosttyResult: ...
def ghostty_render_state_row_iterator_new(
    allocator: GhosttyAllocator, out_iterator: GhosttyRenderStateRowIterator
) -> GhosttyResult: ...
def ghostty_render_state_row_iterator_free(iterator: GhosttyRenderStateRowIterator) -> None: ...
def ghostty_render_state_row_iterator_next(iterator: GhosttyRenderStateRowIterator) -> bool: ...
def ghostty_render_state_row_get(
    iterator: GhosttyRenderStateRowIterator, data: GhosttyRenderStateRowData, out: object
) -> GhosttyResult: ...
def ghostty_render_state_row_set(
    iterator: GhosttyRenderStateRowIterator, option: GhosttyRenderStateRowOption, value: object
) -> GhosttyResult: ...
def ghostty_render_state_row_cells_new(
    allocator: GhosttyAllocator, out_cells: GhosttyRenderStateRowCells
) -> GhosttyResult: ...
def ghostty_render_state_row_cells_free(cells: GhosttyRenderStateRowCells) -> None: ...
def ghostty_render_state_row_cells_next(cells: GhosttyRenderStateRowCells) -> bool: ...
def ghostty_render_state_row_cells_get(
    cells: GhosttyRenderStateRowCells, data: GhosttyRenderStateRowCellsData, out: object
) -> GhosttyResult: ...
