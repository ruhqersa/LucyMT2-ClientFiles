import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/game/premium_private_shop/"

window = {
	"name" : "OfflineShopWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("float",),
	"width" : 184,
	"height" : 120,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 184,
			"height" : 120,

			"children" :
			(
				## ShopSign
				{
					"name" : "ShopSignSlot",
					"type" : "slotbar",

					"x" : -1,
					"y" : 12,

					"horizontal_align" : "center",
					"width" : 162,
					"height" : 18,

					"children" :
					(
						{
							"name" : "ShopSignText",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",

							"text" : "",
						},
					),
				},

				## PositionInfoText
				{
					"name" : "PositionInfoSlot",
					"type" : "slotbar",

					"x" : -1,
					"y" : 37,

					"horizontal_align" : "center",
					"width" : 162,
					"height" : 18,

					"children" :
					(
						{
							"name" : "PosInfoText",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",

							"text" : "",
						},
					),
				},

				## TimeLeftText
				{
					"name" : "TimeLeftSlot",
					"type" : "slotbar",

					"x" : -1,
					"y" : 62,

					"horizontal_align" : "center",

					"width" : 162,
					"height" : 18,

					"children" :
					(
						{
							"name" : "TimeLeftText",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",

							"text" : "",
						},
					),
				},

				## LockButton
				{
					"name" : "LockButton",
					"type" : "button",

					"x" : 7,
					"y" : 87,

					"horizontal_align" : "left",
					"tooltip_text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK,

					"tooltip_x" : 0,
					"tooltip_y" : -10,

					"default_image" : ROOT_PATH + "reopen_button_default.sub",
					"over_image" : ROOT_PATH + "reopen_button_over.sub",
					"down_image" : ROOT_PATH + "reopen_button_down.sub",
				},

				## RenameButton
				{
					"name" : "RenameButton",
					"type" : "button",

					"x" : -3,
					"y" : 87,

					"horizontal_align" : "center",
					"tooltip_text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_RENAME,

					"tooltip_x" : 0,
					"tooltip_y" : -10,

					"default_image" : "d:/ymir work/ui/game/premium_private_shop/modify_button_default.sub",
					"over_image" : "d:/ymir work/ui/game/premium_private_shop/modify_button_over.sub",
					"down_image" : "d:/ymir work/ui/game/premium_private_shop/modify_button_down.sub",
				},

				## CloseButton
				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 63,
					"y" : 87,

					"horizontal_align" : "right",
					"tooltip_text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_CLOSE,

					"tooltip_x" : 0,
					"tooltip_y" : -10,

					"default_image" : ROOT_PATH + "shop_close_button_default.sub",
					"over_image" : ROOT_PATH + "shop_close_button_over.sub",
					"down_image" : ROOT_PATH + "shop_close_button_down.sub",
				},
			),
		},
	),
}

