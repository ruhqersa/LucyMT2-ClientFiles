import net
import player
import item
import snd
import shop
import net
import wndMgr
import app
import chat

import ui
import uiCommon
import mouseModule
import localeInfo
import constInfo

if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiPickMoney
	import time
	import background
	import uiScriptLocale

###################################################################################################
## Shop
class ShopDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.offlineShopWnd = OfflineShopWindow()
			self.priceInputBoard = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __GetRealIndex(self, i):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + i
	
	def Refresh(self):
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemID=self.itemSlotWindow.SetItemSlot
		for i in xrange(shop.SHOP_SLOT_COUNT):
			idx = self.__GetRealIndex(i)
			itemCount = getItemCount(idx)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(idx), itemCount)

		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetItemData(pos, itemID, itemCount, itemPrice)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/shopdialog.py")
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.LoadObject")

		smallTab1 = None
		smallTab2 = None
		smallTab3 = None
		middleTab1 = None
		middleTab2 = None
		
		try:
			GetObject = self.GetChild
			self.itemSlotWindow = GetObject("ItemSlot")
			self.btnBuy = GetObject("BuyButton")
			self.btnSell = GetObject("SellButton")
			self.btnClose = GetObject("CloseButton")
			self.titleBar = GetObject("TitleBar")
			middleTab1 = GetObject("MiddleTab1")
			middleTab2 = GetObject("MiddleTab2")
			smallTab1 = GetObject("SmallTab1")
			smallTab2 = GetObject("SmallTab2")
			smallTab3 = GetObject("SmallTab3")
			if app.ENABLE_OFFLINE_SHOP_SYSTEM:
				self.goldButton = GetObject("MoneySlot")
				self.goldText = GetObject("Money")
				self.goldAmount = 0

				if app.ENABLE_CHEQUE_SYSTEM:
					self.chequeButton = GetObject("Cheque_Slot")
					self.chequeText = GetObject("Cheque")
					self.chequeAmount = 0
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.btnBuy.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnBuy.SetToggleDownEvent(ui.__mem_func__(self.OnBuy))

		self.btnSell.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnSell.SetToggleDownEvent(ui.__mem_func__(self.OnSell))

		self.btnClose.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.goldButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

			self.dlgPickMoney = uiPickMoney.PickMoneyDialog()
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.LoadDialog()
			self.dlgPickMoney.SetMax(10)
			self.dlgPickMoney.Hide()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.smallRadioButtonGroup = ui.RadioButtonGroup.Create([[smallTab1, lambda : self.OnClickTabButton(0), None], [smallTab2, lambda : self.OnClickTabButton(1), None], [smallTab3, lambda : self.OnClickTabButton(2), None]])
		self.middleRadioButtonGroup = ui.RadioButtonGroup.Create([[middleTab1, lambda : self.OnClickTabButton(0), None], [middleTab2, lambda : self.OnClickTabButton(1), None]])

		self.__HideMiddleTabs()
		self.__HideSmallTabs()
		
		self.tabIdx = 0
		self.coinType = shop.SHOP_COIN_TYPE_GOLD
		
		self.Refresh()
	
	def __ShowBuySellButton(self):
		self.btnBuy.Show()
		self.btnSell.Show()
		
	def __ShowMiddleTabs(self):
		self.middleRadioButtonGroup.Show()
	
	def __ShowSmallTabs(self):
		self.smallRadioButtonGroup.Show()
	
	def __HideBuySellButton(self):
		self.btnBuy.Hide()
		self.btnSell.Hide()
	
	def __HideMiddleTabs(self):
		self.middleRadioButtonGroup.Hide()
	
	def __HideSmallTabs(self):
		self.smallRadioButtonGroup.Hide()
		
	def __SetTabNames(self):
		if shop.GetTabCount() == 2:
			self.middleRadioButtonGroup.SetText(0, shop.GetTabName(0))
			self.middleRadioButtonGroup.SetText(1, shop.GetTabName(1))
		elif shop.GetTabCount() == 3:
			self.smallRadioButtonGroup.SetText(0, shop.GetTabName(0))
			self.smallRadioButtonGroup.SetText(1, shop.GetTabName(1))
			self.smallRadioButtonGroup.SetText(2, shop.GetTabName(2))
	 
 
	def Destroy(self):
		self.Close()
		self.ClearDictionary()

		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.btnBuy = 0
		self.btnSell = 0
		self.btnClose = 0
		self.titleBar = 0
		self.questionDialog = None
		self.popup = None
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.offlineShopWnd.Destroy()
			self.offlineShopWnd = None
			self.goldButton = None
			self.goldText = None
			if app.ENABLE_CHEQUE_SYSTEM:
				self.chequeButton = None
				self.chequeText = None
			self.dlgPickMoney.Destroy()
			self.dlgPickMoney = None
			self.priceInputBoard = None

	def Open(self, vid, extraInfo = False):

		isPrivateShop = False
		isMainPlayerPrivateShop = False

		import chr
		if chr.IsNPC(vid):
			isPrivateShop = False
		else:
			isPrivateShop = True

		if player.IsMainCharacterIndex(vid):

			isMainPlayerPrivateShop = True

			self.btnBuy.Hide()
			self.btnSell.Hide()
			self.btnClose.Show()

		else:

			isMainPlayerPrivateShop = False

			self.btnBuy.Show()
			self.btnSell.Show()
			self.btnClose.Hide()

		shop.Open(isPrivateShop, isMainPlayerPrivateShop)

		self.tabIdx = 0

		if isPrivateShop:
			self.__HideMiddleTabs()
			self.__HideSmallTabs()
		else:
			if shop.GetTabCount() == 1:
				self.__ShowBuySellButton()
				self.__HideMiddleTabs()
				self.__HideSmallTabs()
			elif shop.GetTabCount() == 2:
				self.__HideBuySellButton()
				self.__ShowMiddleTabs()
				self.__HideSmallTabs()
				self.__SetTabNames()
				self.middleRadioButtonGroup.OnClick(0)
			elif shop.GetTabCount() == 3:
				self.__HideBuySellButton()
				self.__HideMiddleTabs()
				self.__ShowSmallTabs()
				self.__SetTabNames()
				self.middleRadioButtonGroup.OnClick(1)

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if shop.IsOwner():
				self.__HideBuySellButton()
				self.goldButton.Show()
				self.goldAmount = shop.GetGoldAmount()
				self.goldText.SetText(localeInfo.NumberToMoney(self.goldAmount))
				if app.ENABLE_CHEQUE_SYSTEM:
					self.chequeButton.Show()
					self.chequeAmount = shop.GetChequeAmount()
					self.chequeText.SetText(localeInfo.NumberToCheque(self.chequeAmount))
				x, y = self.GetGlobalPosition()
				self.offlineShopWnd.Open(x, y, extraInfo)
				self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_PICK_UP)
			else:
				self.goldButton.Hide()
				if app.ENABLE_CHEQUE_SYSTEM:
					self.chequeButton.Hide()
				self.offlineShopWnd.Hide()
				self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		self.Refresh()
		self.SetTop()
		
		self.Show()

		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()

	def Close(self):
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		if self.questionDialog:
			self.OnCloseQuestionDialog()
		shop.Close()
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.offlineShopWnd.Close()
			self.dlgPickMoney.Close()
		net.SendShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()

	def GetIndexFromSlotPos(self, slotPos):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + slotPos
		
	def OnClickTabButton(self, idx):
		self.tabIdx = idx
		self.Refresh()
		
	def AskClosePrivateShop(self):
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		return True

	def OnClosePrivateShop(self):
		net.SendChatPacket("/close_shop")
		self.OnCloseQuestionDialog()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
		app.SetCursor(app.BUY)
		self.btnSell.SetUp()

	def OnSell(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)
		app.SetCursor(app.SELL)
		self.btnBuy.SetUp()

	def CancelShopping(self):
		self.btnBuy.SetUp()
		self.btnSell.SetUp()
		app.SetCursor(app.NORMAL)

	def __OnClosePopupDialog(self):
		self.pop = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## ¿ëÈ¥¼® ÆÈ¸®´Â ±â´É Ãß°¡.
	def SellAttachedItem(self):

		if shop.IsPrivateShop():
			mouseModule.mouseController.DeattachObject()
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedCount = mouseModule.mouseController.GetAttachedItemCount()
		if localeInfo.IsBRAZIL() == 0:
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
		
		if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:

			if localeInfo.IsBRAZIL():
				itemIndex = player.GetItemIndex(attachedSlotPos)
				item.SelectItem(itemIndex)
			else:
				item.SelectItem(attachedItemIndex)
			
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return
				
			itemtype = player.INVENTORY

			if localeInfo.IsBRAZIL() == 0:
				if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
					itemtype = player.DRAGON_SOUL_INVENTORY
			
			if player.IsValuableItem(itemtype, attachedSlotPos):

				itemPrice = item.GetISellItemPrice()

				if item.Is1GoldItem():
					itemPrice = attachedCount / itemPrice / 5
				else:
					itemPrice = itemPrice * max(1, attachedCount) / 5

				itemName = item.GetItemName()

				questionDialog = uiCommon.QuestionDialog()
				questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, attachedCount, itemPrice))

				questionDialog.SetAcceptEvent(lambda arg1=attachedSlotPos, arg2=attachedCount, arg3 = itemtype: self.OnSellItem(arg1, arg2, arg3))
				questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				questionDialog.Open()
				self.questionDialog = questionDialog
		
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			else:
				self.OnSellItem(attachedSlotPos, attachedCount, itemtype)

		else:
			snd.PlaySound("sound/ui/loginfail.wav")

		mouseModule.mouseController.DeattachObject()

	def OnSellItem(self, slotPos, count, itemtype):
		net.SendShopSellPacketNew(slotPos, count, itemtype)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
			
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			if app.ENABLE_OFFLINE_SHOP_SYSTEM:
				if shop.IsOwner():
					attachedSlotType = mouseModule.mouseController.GetAttachedType()
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					mouseModule.mouseController.DeattachObject()

					if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
						return

					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

					itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
					item.SelectItem(itemVNum)

					if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
						return

					priceInputBoard = uiCommon.MoneyInputDialog()
					priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
					priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
					priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
					priceInputBoard.Open()

					self.priceInputBoard = priceInputBoard
					self.priceInputBoard.itemVNum = itemVNum
					self.priceInputBoard.sourceWindowType = attachedInvenType
					self.priceInputBoard.sourceSlotPos = attachedSlotPos
					self.priceInputBoard.targetSlotPos = selectedSlotPos
				else:
					self.SellAttachedItem()
			else:
				self.SellAttachedItem()

	def UnselectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		if shop.IsPrivateShop():
			self.AskBuyItem(selectedSlotPos)
		else:
			if app.ENABLE_OFFLINE_SHOP_SYSTEM and shop.IsOwner():
				net.SendShopWithdrawItemPacket(self.__GetRealIndex(selectedSlotPos))
			else:
				self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		isAttached = mouseModule.mouseController.isAttached()
		selectedSlotPos = self.__GetRealIndex(selectedSlotPos)
		if isAttached:
			self.SellAttachedItem()

		else:

			if True == shop.IsMainPlayerPrivateShop():
				return

			curCursorNum = app.GetCursor()
			if app.BUY == curCursorNum:
				self.AskBuyItem(selectedSlotPos)

			elif app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)

			else:
				selectedItemID = shop.GetItemID(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_SHOP
				if shop.IsPrivateShop():
					type = player.SLOT_TYPE_PRIVATE_SHOP

				mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		if app.ENABLE_OFFLINE_SHOP_SYSTEM and shop.IsOwner():
			net.SendShopWithdrawItemPacket(self.__GetRealIndex(slotPos))
			return
		slotPos = self.__GetRealIndex(slotPos)
		
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uiCommon.QuestionDialog()
		itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)))
		itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.Open()
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):

		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverInItem(self, slotIndex):
		slotIndex = self.__GetRealIndex(slotIndex)
		if mouseModule.mouseController.isAttached():
			return

		if 0 != self.tooltipItem:
			if shop.SHOP_COIN_TYPE_GOLD == shop.GetTabCoinType(self.tabIdx):
				self.tooltipItem.SetShopItem(slotIndex)
			else: 
				self.tooltipItem.SetShopItemBySecondaryCoin(slotIndex)
	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		USE_SHOP_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > USE_SHOP_LIMIT_RANGE:
			self.Close()

		self.offlineShopWnd.UpdateTime()

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def OnMoveWindow(self, x, y):
			self.offlineShopWnd.UpdatePosition(x, y)

		if app.ENABLE_CHEQUE_SYSTEM:
			def OpenPickMoneyDialog(self):
				self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
				self.dlgPickMoney.Open(self.goldAmount, self.chequeAmount)
		else:
			def OpenPickMoneyDialog(self):
				self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
				self.dlgPickMoney.Open(self.goldAmount)

		def UpdateGold(self, gold):
			self.goldAmount = gold
			self.goldText.SetText(localeInfo.NumberToMoney(gold))

		if app.ENABLE_CHEQUE_SYSTEM:
			def UpdateCheque(self, cheque):
				self.chequeAmount = cheque
				self.chequeText.SetText(localeInfo.NumberToCheque(cheque))

		def UpdateLock(self, lock):
			self.offlineShopWnd.UpdateLock(lock)

		def UpdateTime(self, timeLeft):
			self.offlineShopWnd.SetTime(timeLeft)

		def UpdateSign(self, sign):
			self.offlineShopWnd.UpdateSign(sign)

		def OpenOfflineShop(self, sign, channel, index, x, y, time, update):
			if update and self.IsShow():
				self.Open(0, True)
			elif not update:
				self.Open(0, True)

			self.offlineShopWnd.SetShopInfo(sign, channel, index, x, y, time, update)

		if app.ENABLE_CHEQUE_SYSTEM:
			def OnPickMoney(self, gold, cheque):
				if gold >= 1:
					net.SendShopWithdrawGoldPacket(gold)

				if cheque >= 1:
					net.SendShopWithdrawChequePacket(cheque)
		else:
			def OnPickMoney(self, gold):
				net.SendShopWithdrawGoldPacket(gold)

		def AcceptInputPrice(self):
			if not self.priceInputBoard:
				return True

			text = self.priceInputBoard.GetText()

			if app.ENABLE_CHEQUE_SYSTEM:
				cheText = self.priceInputBoard.GetChequeText()
				if not text and not cheText:
					return True

				if not text.isdigit() and not cheText.isdigit():
					return True

				if int(text) <= 0 and int(cheText) <= 0:
					return True
			else:
				if not text:
					return True

				if not text.isdigit():
					return True

				if int(text) <= 0:
					return True

			attachedInvenType = self.priceInputBoard.sourceWindowType
			sourceSlotPos = self.priceInputBoard.sourceSlotPos
			targetSlotPos = self.priceInputBoard.targetSlotPos
			price = int(self.priceInputBoard.GetText())
			if app.ENABLE_CHEQUE_SYSTEM:
				cheque = int(self.priceInputBoard.GetChequeText())

			if app.ENABLE_CHEQUE_SYSTEM:
				net.SendShopAddItemPacket(attachedInvenType, sourceSlotPos, targetSlotPos, price, cheque)
			else:
				net.SendShopAddItemPacket(attachedInvenType, sourceSlotPos, targetSlotPos, price)

			self.priceInputBoard = None

			return True

		def CancelInputPrice(self):
			self.priceInputBoard = None
			return True

if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	class OfflineShopWindow(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def LoadWindow(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/offlineshop.py")
			except:
				import exception
				exception.Abort("OfflineShopWindow.LoadDialog.LoadObject")

			try:
				GetObject = self.GetChild
				self.board = GetObject("board")
				self.lockButton = GetObject("LockButton")
				self.renameButton = GetObject("RenameButton")
				self.closeButton = GetObject("CloseButton")
				self.signText = GetObject("ShopSignText")
				self.posInfoText = GetObject("PosInfoText")
				self.timeLeftText = GetObject("TimeLeftText")
			except:
				import exception
				exception.Abort("OfflineShopWindow.LoadDialog.BindObject")

			self.lockButton.SetEvent(ui.__mem_func__(self.SetLock))
			self.renameButton.SetEvent(ui.__mem_func__(self.OnPressChange))
			self.closeButton.SetEvent(ui.__mem_func__(self.CloseShop))

			self.expireTime = 0

			self.signInputBoard = uiCommon.InputDialogWithDescription()
			self.signInputBoard.SetTitle(uiScriptLocale.OFFLINE_SHOP_INPUT_SIGN_TITLE)
			self.signInputBoard.SetMaxLength(25)
			self.signInputBoard.SetBoardWidth(318 - 64)
			self.signInputBoard.SetSlotWidth(203)
			self.signInputBoard.SetAcceptEvent(ui.__mem_func__(self.ChangeSign))
			self.signInputBoard.SetCancelEvent(ui.__mem_func__(self.CloseSignBoard))

			self.questionDialog = None

		def Destroy(self):
			self.ClearDictionary()
			self.lockButton = None
			self.closeButton = None
			self.signText = None
			self.timeLeftText = None
			self.posInfoText = None
			self.renameButton = None
			self.signInputBoard.Close()
			self.signInputBoard = None
			self.questionDialog = None

		def Open(self, x, y, extraInfo):
			if extraInfo:
				self.closeButton.Hide()
			else:
				self.closeButton.Show()

			self.isLocked = shop.IsLocked()
			self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_UNLOCK if self.isLocked else uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK)

			self.Show()
			self.SetPosition(x, y + 328)
			self.SetTop()

		def SetShopInfo(self, sign, channel, index, x, y, timeLeft, update):
			self.expireTime = time.clock() + timeLeft

			(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(x, y)
			localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")
			self.posInfoText.SetText("CH %d, %s (%d, %d)" % (channel, localeMapName, int(x - xBase) / 100, int(y - yBase) / 100))

			self.signInputBoard.SetDescription(uiScriptLocale.OFFLINE_SHOP_INPUT_SIGN_DESC % sign)
			self.signText.SetText(sign if len(sign) < 18 else sign[:17] + "...")

		def Close(self):
			self.OnCloseQuestionDialog()
			self.Hide()

		def UpdatePosition(self, x, y):
			if self.IsShow():
				self.SetPosition(x, y + 328)
				self.SetTop()

		def SetLock(self, arg = True):
			if self.expireTime <= time.clock() and arg:
				questionDialog = uiCommon.QuestionDialog()
				questionDialog.SetText(uiScriptLocale.OFFLINE_SHOP_RENEW_CONFIRM)
				questionDialog.SetAcceptEvent(lambda arg = False: self.SetLock(arg))
				questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				questionDialog.Open()
				self.questionDialog = questionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			else:
				net.SendShopLockPacket(not self.isLocked)
				self.OnCloseQuestionDialog()

		def UpdateLock(self, lock):
			self.isLocked = lock

			if self.expireTime <= time.clock():
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_RENEW)
			else:
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_UNLOCK if self.isLocked else uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK)

		def SetTime(self, timeLeft):
			self.expireTime = time.clock() + timeLeft

		def UpdateTime(self):
			expired = self.expireTime <= time.clock()

			m, s = divmod(self.expireTime - time.clock(), 60)
			h, m = divmod(m, 60)
			d, h = divmod(h, 24)

			self.timeLeftText.SetFontColor(0.5411, 0.7254, 0.5568)
			self.timeLeftText.SetText(uiScriptLocale.OFFLINE_SHOP_TIME_LEFT % ((d, h, m) if not expired else (0, 0, 0)))

			if expired:
				self.timeLeftText.SetFontColor(0.9, 0.4745, 0.4627)
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_RENEW)

		def UpdateSign(self, sign):
			self.signInputBoard.SetDescription(uiScriptLocale.OFFLINE_SHOP_INPUT_SIGN_DESC % sign)
			self.signText.SetText(sign if len(sign) < 18 else sign[:17] + "...")

		def CloseShop(self):
			net.SendCloseShopPacket()

		def OnPressChange(self):
			self.signInputBoard.Open()

		def ChangeSign(self):
			net.SendShopChangeSignPacket(self.signInputBoard.GetText())
			self.CloseSignBoard()

		def CloseSignBoard(self):
			self.signInputBoard.Hide()
			self.signInputBoard.inputValue.SetText("")

		def OnCloseQuestionDialog(self):
			if not self.questionDialog:
				return

			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)



class MallPageDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def Open(self):
		scriptLoader = ui.PythonScriptLoader()
		scriptLoader.LoadScriptFile(self, "uiscript/mallpagedialog.py")

		self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))
		
		(x, y)=self.GetGlobalPosition()
		x+=10
		y+=30
		
		MALL_PAGE_WIDTH = 600
		MALL_PAGE_HEIGHT = 480
		
		app.ShowWebPage(
			"http://metin2.co.kr/08_mall/game_mall/login_fail.htm", 
			(x, y, x+MALL_PAGE_WIDTH, y+MALL_PAGE_HEIGHT))

		self.Lock()
		self.Show()
		
	def Close(self):			
		app.HideWebPage()
		self.Unlock()
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
