local compe = {}

function compe:init()
    if not packer_plugins["plenary.nvim"].loaded then
        vim.cmd [[packadd plenary.nvim]]
    end
    require("compe").setup(
        {
            enabled = true,
            autocomplete = true,
            debug = false,
            min_length = 1,
            preselect = "enable",
            throttle_time = 80,
            source_timeout = 200,
            resolve_timeout = 800,
            incomplete_delay = 400,
            max_abbr_width = 100,
            max_kind_width = 100,
            max_menu_width = 100,
            documentation = {
                border = {"", "", "", " ", "", "", "", " "}, -- the border option is the same as `|help nvim_open_win|`
                winhighlight = "NormalFloat:CompeDocumentation,FloatBorder:CompeDocumentationBorder",
                max_width = 120,
                min_width = 60,
                max_height = math.floor(vim.o.lines * 0.3),
                min_height = 1
            },
            source = {
                tabnine = false,
                nvim_lsp = true,
                luasnip = true,
                zsh = true,
                path = true,
                calc = true,
                nvim_lua = false,
                snippets_nvim = false,
                buffer = false,
                vsnip = false,
                spell = false,
                tags = false,
                treesitter = false
            }
        }
    )
end

return compe