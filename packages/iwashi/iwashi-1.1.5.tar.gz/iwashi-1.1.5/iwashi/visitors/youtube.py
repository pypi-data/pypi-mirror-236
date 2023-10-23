import json
import re
from pathlib import Path
from typing import Dict, List, TypedDict, Union
from urllib import parse

import bs4
import requests

from ..helper import BASE_HEADERS, HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Youtube(SiteVisitor):
    NAME = "Youtube"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"(m\.)?(youtube\.com|youtu\.be)", re.IGNORECASE
    )

    def _channel_by_video(self, video_id: str) -> str | None:
        res = requests.get(
            "https://www.youtube.com/watch",
            params={"v": video_id},
            headers=BASE_HEADERS,
        )
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        author = soup.select_one("span[itemprop=author]")
        if author is None:
            return None
        author_url = author.select_one("link[itemprop=url]")
        if author_url is None:
            return None
        return author_url.attrs.get("href")

    def _channel_by_url(self, url: str) -> str | None:
        res = requests.get(
            url,
            headers=BASE_HEADERS
            | {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "ja",
            },
        )
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        """
        metadata.channelMetadataRenderer.vanityChannelUrl
        """
        for script in soup.find_all("script"):
            if script.text.startswith("var ytInitialData = "):
                break
        else:
            raise NotImplementedError("Could not find ytInitialData")
        root: Root = json.loads(script.text[script.text.index("{") : -1])
        Path("dump.json").write_text(json.dumps(root, indent=2))
        return root["header"]["c4TabbedHeaderRenderer"]["navigationEndpoint"][
            "commandMetadata"
        ]["webCommandMetadata"]["url"].split("@")[-1]

    def normalize(self, url: str) -> str | None:
        uri = parse.urlparse(url)
        if uri.hostname == "youtu.be":
            return self._channel_by_video(uri.path[1:])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return f"https://www.youtube.com/{type}"
        if type == "watch":
            return self._channel_by_video(parse.parse_qs(uri.query)["v"][0])
        if type in ("channel", "user", "c"):
            return self._channel_by_url(url)
        return url

    def visit(self, url, context: Context):
        about_res = requests.get(f"{url}/about", headers=BASE_HEADERS)
        soup = bs4.BeautifulSoup(about_res.text, "html.parser")
        for script in soup.find_all("script"):
            if script.text.startswith("var ytInitialData = "):
                break
        else:
            return
        root: Root = json.loads(script.text[len("var ytInitialData = ") : -1])

        links = []
        about = None
        for tab in root["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]:
            if "content" in tab:
                pass
            if "tabRenderer" not in tab:
                continue
            *_, endpoint = tab["tabRenderer"]["endpoint"]["commandMetadata"][
                "webCommandMetadata"
            ]["url"].split("/")
            if endpoint != "about":
                continue
            if "content" not in tab["tabRenderer"]:
                raise NotImplementedError("Could not find content")
            for section in tab["tabRenderer"]["content"]["sectionListRenderer"][
                "contents"
            ]:
                for item in section["itemSectionRenderer"]["contents"]:
                    if "channelAboutFullMetadataRenderer" not in item:
                        raise NotImplementedError(
                            "Could not find channelAboutFullMetadataRenderer"
                        )
                    about = item["channelAboutFullMetadataRenderer"]
                    if "links" not in about:
                        break
                    for link in about["links"]:
                        if "channelExternalLinkViewModel" not in link:
                            continue
                        for command in link["channelExternalLinkViewModel"]["link"][
                            "commandRuns"
                        ]:
                            link = command["onTap"]["innertubeCommand"]["urlEndpoint"][
                                "url"
                            ]
                            uri = parse.urlparse(link)
                            if uri.path == "/redirect":
                                link = parse.unquote(parse.parse_qs(uri.query)["q"][0])
                            links.append(link)
            break
        else:
            raise NotImplementedError("Could not find about")

        profile_picture = None
        if "avatar" in root["header"]["c4TabbedHeaderRenderer"]:
            profile_picture = root["header"]["c4TabbedHeaderRenderer"]["avatar"][
                "thumbnails"
            ][0]["url"]

        description = None
        if about and "description" in about:
            description = about["description"]["simpleText"]

        name = root["header"]["c4TabbedHeaderRenderer"]["title"]

        context.create_result(
            "Youtube",
            url=url,
            score=1.0,
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        for url in links:
            context.visit(url)


class ParamsItem(TypedDict):
    key: str
    value: str


class ServicetrackingparamsItem(TypedDict):
    service: str
    params: List[ParamsItem]


class Mainappwebresponsecontext(TypedDict):
    datasyncId: str
    loggedOut: bool
    trackingParam: str


class Webresponsecontextextensiondata(TypedDict):
    hasDecorated: bool


class Responsecontext(TypedDict):
    serviceTrackingParams: List[ServicetrackingparamsItem]
    maxAgeSeconds: int
    mainAppWebResponseContext: Mainappwebresponsecontext
    webResponseContextExtensionData: Webresponsecontextextensiondata


class Webcommandmetadata(TypedDict):
    url: str
    webPageType: str
    rootVe: int
    apiUrl: str


class Commandmetadata(TypedDict):
    webCommandMetadata: Webcommandmetadata


class Browseendpoint(TypedDict):
    browseId: str
    params: str
    canonicalBaseUrl: str


class Endpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint


class Tabrenderer(TypedDict):
    endpoint: Endpoint
    title: str
    trackingParams: str


class TabsItem(TypedDict):
    tabRenderer: Tabrenderer


class Description(TypedDict):
    simpleText: str


class RunsItem(TypedDict):
    text: str


class Joineddatetext(TypedDict):
    runs: List[RunsItem]


class ThumbnailsItem(TypedDict):
    url: str
    width: int
    height: int


class Avatar(TypedDict):
    thumbnails: List[ThumbnailsItem]


class Webcommandmetadata0(TypedDict):
    sendPost: bool


class Commandmetadata0(TypedDict):
    webCommandMetadata: Webcommandmetadata0


class Webcommandmetadata1(TypedDict):
    sendPost: bool
    apiUrl: str


class Commandmetadata1(TypedDict):
    webCommandMetadata: Webcommandmetadata1


class Flagendpoint(TypedDict):
    flagAction: str


class Serviceendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    flagEndpoint: Flagendpoint


class Accessibility(TypedDict):
    label: str


class Accessibilitydata(TypedDict):
    accessibilityData: Accessibility


class Buttonrenderer(TypedDict):
    style: str
    size: str
    text: Joineddatetext
    serviceEndpoint: Serviceendpoint
    accessibility: Accessibility
    trackingParams: str
    accessibilityData: Accessibilitydata


class Confirmbutton(TypedDict):
    buttonRenderer: Buttonrenderer


class Buttonrenderer0(TypedDict):
    style: str
    size: str
    text: Joineddatetext
    accessibility: Accessibility
    trackingParams: str
    accessibilityData: Accessibilitydata


class Cancelbutton(TypedDict):
    buttonRenderer: Buttonrenderer0


class Confirmdialogrenderer(TypedDict):
    title: Joineddatetext
    trackingParams: str
    dialogMessages: List[Joineddatetext]
    confirmButton: Confirmbutton
    cancelButton: Cancelbutton
    primaryIsCancel: bool


class Popup(TypedDict):
    confirmDialogRenderer: Confirmdialogrenderer


class Openpopupaction(TypedDict):
    popup: Popup
    popupType: str


class ActionsItem(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction


class Signalserviceendpoint(TypedDict):
    signal: str
    actions: List[ActionsItem]


class Defaultserviceendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint


class Togglemenuserviceitemrenderer(TypedDict):
    defaultText: Joineddatetext
    defaultServiceEndpoint: Defaultserviceendpoint
    toggledText: Joineddatetext
    toggledServiceEndpoint: Defaultserviceendpoint
    trackingParams: str
    isToggled: bool
    toggleMenuServiceItemEntityKey: str


class ItemsItem(TypedDict):
    toggleMenuServiceItemRenderer: Togglemenuserviceitemrenderer


class Menuserviceitemrenderer(TypedDict):
    text: Joineddatetext
    serviceEndpoint: Defaultserviceendpoint
    trackingParams: str


class ItemsItem0(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer


class Getreportformendpoint(TypedDict):
    params: str


class Serviceendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    getReportFormEndpoint: Getreportformendpoint


class Multipagemenurenderer(TypedDict):
    trackingParams: str
    style: str
    showLoadingSpinner: bool


class Popup0(TypedDict):
    multiPageMenuRenderer: Multipagemenurenderer


class Openpopupaction0(TypedDict):
    popup: Popup0
    popupType: str
    uniqueId: str
    beReused: bool


class Command(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction0


class Menuserviceitemrenderer0(TypedDict):
    text: Joineddatetext
    serviceEndpoint: Serviceendpoint0
    trackingParams: str
    command: Command


class ItemsItem1(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer0


class Menupopuprenderer(TypedDict):
    items: List[Union[ItemsItem, ItemsItem0, ItemsItem1]]


class Popup1(TypedDict):
    menuPopupRenderer: Menupopuprenderer


class Openpopupaction1(TypedDict):
    popup: Popup1
    popupType: str


class ActionsItem0(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction1


class Signalserviceendpoint0(TypedDict):
    signal: str
    actions: List[ActionsItem0]


class Serviceendpoint1(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint0


class Icon(TypedDict):
    iconType: str


class Buttonrenderer1(TypedDict):
    style: str
    size: str
    serviceEndpoint: Serviceendpoint1
    icon: Icon
    accessibility: Accessibility
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibilitydata


class ActionbuttonsItem(TypedDict):
    buttonRenderer: Buttonrenderer1


class Unifiedsharepanelrenderer(TypedDict):
    trackingParams: str
    showLoadingSpinner: bool


class Popup2(TypedDict):
    unifiedSharePanelRenderer: Unifiedsharepanelrenderer


class Openpopupaction2(TypedDict):
    popup: Popup2
    popupType: str
    beReused: bool


class CommandsItem(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction2


class Shareentityserviceendpoint(TypedDict):
    serializedShareEntity: str
    commands: List[CommandsItem]


class Command0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    shareEntityServiceEndpoint: Shareentityserviceendpoint


class Menuserviceitemrenderer1(TypedDict):
    text: Joineddatetext
    trackingParams: str
    command: Command0


class ItemsItem2(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer1


class Notificationactionrenderer(TypedDict):
    responseText: Joineddatetext
    trackingParams: str


class Popup3(TypedDict):
    notificationActionRenderer: Notificationactionrenderer


class Openpopupaction3(TypedDict):
    popup: Popup3
    popupType: str


class ActionsItem1(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction3


class Signalserviceendpoint1(TypedDict):
    signal: str
    actions: List[ActionsItem1]


class SuccessactionsItem(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint1


class Copytextendpoint(TypedDict):
    text: str
    successActions: List[SuccessactionsItem]


class Command1(TypedDict):
    clickTrackingParams: str
    copyTextEndpoint: Copytextendpoint


class Menuserviceitemrenderer2(TypedDict):
    text: Joineddatetext
    trackingParams: str
    command: Command1


class ItemsItem3(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer2


class Menupopuprenderer0(TypedDict):
    items: List[Union[ItemsItem2, ItemsItem3]]


class Popup4(TypedDict):
    menuPopupRenderer: Menupopuprenderer0


class Openpopupaction4(TypedDict):
    popup: Popup4
    popupType: str


class ActionsItem2(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction4


class Signalserviceendpoint2(TypedDict):
    signal: str
    actions: List[ActionsItem2]


class Command2(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint2


class Buttonrenderer2(TypedDict):
    icon: Icon
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibilitydata
    command: Command2


class ActionbuttonsItem0(TypedDict):
    buttonRenderer: Buttonrenderer2


class Onbusinessemailrevealclickcommand(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    revealBusinessEmailCommand: Dict


class Title(TypedDict):
    content: str


class Webcommandmetadata2(TypedDict):
    url: str
    webPageType: str
    rootVe: int


class Commandmetadata2(TypedDict):
    webCommandMetadata: Webcommandmetadata2


class Urlendpoint(TypedDict):
    url: str
    nofollow: bool


class Innertubecommand(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    urlEndpoint: Urlendpoint


class Ontap(TypedDict):
    innertubeCommand: Innertubecommand


class CommandrunsItem(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap


class Link(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem]


class Channelexternallinkviewmodel(TypedDict):
    title: Title
    link: Link


class LinksItem(TypedDict):
    channelExternalLinkViewModel: Channelexternallinkviewmodel


class Urlendpoint0(TypedDict):
    url: str
    target: str
    nofollow: bool


class Innertubecommand0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    urlEndpoint: Urlendpoint0


class Ontap0(TypedDict):
    innertubeCommand: Innertubecommand0


class CommandrunsItem0(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap0


class Link0(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem0]


class Channelexternallinkviewmodel0(TypedDict):
    title: Title
    link: Link0


class LinksItem0(TypedDict):
    channelExternalLinkViewModel: Channelexternallinkviewmodel0


class Channelaboutfullmetadatarenderer(TypedDict):
    description: Description
    viewCountText: Description
    joinedDateText: Joineddatetext
    canonicalChannelUrl: str
    bypassBusinessEmailCaptcha: bool
    title: Description
    avatar: Avatar
    showDescription: bool
    descriptionLabel: Joineddatetext
    detailsLabel: Joineddatetext
    primaryLinksLabel: Joineddatetext
    statsLabel: Joineddatetext
    actionButtons: List[Union[ActionbuttonsItem, ActionbuttonsItem0]]
    channelId: str
    onBusinessEmailRevealClickCommand: Onbusinessemailrevealclickcommand
    links: List[Union[LinksItem, LinksItem0]]


class ContentsItem(TypedDict):
    channelAboutFullMetadataRenderer: Channelaboutfullmetadatarenderer


class Itemsectionrenderer(TypedDict):
    contents: List[ContentsItem]
    trackingParams: str


class ContentsItem0(TypedDict):
    itemSectionRenderer: Itemsectionrenderer


class Sectionlistrenderer(TypedDict):
    contents: List[ContentsItem0]
    trackingParams: str
    disablePullToRefresh: bool


class Content(TypedDict):
    sectionListRenderer: Sectionlistrenderer


class Tabrenderer0(TypedDict):
    endpoint: Endpoint
    title: str
    selected: bool
    content: Content
    trackingParams: str


class TabsItem0(TypedDict):
    tabRenderer: Tabrenderer0


class Expandabletabrenderer(TypedDict):
    endpoint: Endpoint
    title: str
    selected: bool


class TabsItem1(TypedDict):
    expandableTabRenderer: Expandabletabrenderer


class Twocolumnbrowseresultsrenderer(TypedDict):
    tabs: List[Union[TabsItem, TabsItem0, TabsItem1]]


class Contents(TypedDict):
    twoColumnBrowseResultsRenderer: Twocolumnbrowseresultsrenderer


class Browseendpoint0(TypedDict):
    browseId: str
    canonicalBaseUrl: str


class Navigationendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint0


class Metadatabadgerenderer(TypedDict):
    icon: Icon
    style: str
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibility


class BadgesItem(TypedDict):
    metadataBadgeRenderer: Metadatabadgerenderer


class Urlendpoint1(TypedDict):
    url: str


class Innertubecommand1(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    urlEndpoint: Urlendpoint1


class Ontap1(TypedDict):
    innertubeCommand: Innertubecommand1


class CommandrunsItem1(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap1


class Firstlink(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem1]


class Ontap2(TypedDict):
    innertubeCommand: Endpoint


class CommandrunsItem2(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap2


class More(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem2]


class Channelheaderlinksviewmodel(TypedDict):
    firstLink: Firstlink
    more: More


class Headerlinks(TypedDict):
    channelHeaderLinksViewModel: Channelheaderlinksviewmodel


class Buttonrenderer3(TypedDict):
    style: str
    size: str
    isDisabled: bool
    icon: Icon
    accessibility: Accessibility
    trackingParams: str
    accessibilityData: Accessibilitydata


class State(TypedDict):
    buttonRenderer: Buttonrenderer3


class StatesItem(TypedDict):
    stateId: int
    nextStateId: int
    state: State


class Serviceendpoint2(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    modifyChannelNotificationPreferenceEndpoint: Getreportformendpoint


class Menuserviceitemrenderer3(TypedDict):
    text: Description
    icon: Icon
    serviceEndpoint: Serviceendpoint2
    trackingParams: str
    isSelected: bool


class ItemsItem4(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer3


class Unsubscribeendpoint(TypedDict):
    channelIds: List[str]
    params: str


class Serviceendpoint3(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    unsubscribeEndpoint: Unsubscribeendpoint


class Buttonrenderer4(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Joineddatetext
    serviceEndpoint: Serviceendpoint3
    accessibility: Accessibility
    trackingParams: str


class Confirmbutton0(TypedDict):
    buttonRenderer: Buttonrenderer4


class Buttonrenderer5(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Joineddatetext
    accessibility: Accessibility
    trackingParams: str


class Cancelbutton0(TypedDict):
    buttonRenderer: Buttonrenderer5


class Confirmdialogrenderer0(TypedDict):
    trackingParams: str
    dialogMessages: List[Joineddatetext]
    confirmButton: Confirmbutton0
    cancelButton: Cancelbutton0
    primaryIsCancel: bool


class Popup5(TypedDict):
    confirmDialogRenderer: Confirmdialogrenderer0


class Openpopupaction5(TypedDict):
    popup: Popup5
    popupType: str


class ActionsItem3(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction5


class Signalserviceendpoint3(TypedDict):
    signal: str
    actions: List[ActionsItem3]


class Serviceendpoint4(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint3


class Menuserviceitemrenderer4(TypedDict):
    text: Joineddatetext
    icon: Icon
    serviceEndpoint: Serviceendpoint4
    trackingParams: str


class ItemsItem5(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer4


class Menupopuprenderer1(TypedDict):
    items: List[Union[ItemsItem4, ItemsItem5]]


class Popup6(TypedDict):
    menuPopupRenderer: Menupopuprenderer1


class Openpopupaction6(TypedDict):
    popup: Popup6
    popupType: str


class CommandsItem0(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction6


class Commandexecutorcommand(TypedDict):
    commands: List[CommandsItem0]


class Command3(TypedDict):
    clickTrackingParams: str
    commandExecutorCommand: Commandexecutorcommand


class Subscriptionnotificationtogglebuttonrenderer(TypedDict):
    states: List[StatesItem]
    currentStateId: int
    trackingParams: str
    command: Command3
    targetId: str
    secondaryIcon: Icon


class Notificationpreferencebutton(TypedDict):
    subscriptionNotificationToggleButtonRenderer: Subscriptionnotificationtogglebuttonrenderer


class OnsubscribeendpointsItem(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    subscribeEndpoint: Unsubscribeendpoint


class Subscribebuttonrenderer(TypedDict):
    buttonText: Joineddatetext
    subscribed: bool
    enabled: bool
    type: str
    channelId: str
    showPreferences: bool
    subscribedButtonText: Joineddatetext
    unsubscribedButtonText: Joineddatetext
    trackingParams: str
    unsubscribeButtonText: Joineddatetext
    subscribeAccessibility: Accessibilitydata
    unsubscribeAccessibility: Accessibilitydata
    notificationPreferenceButton: Notificationpreferencebutton
    subscribedEntityKey: str
    onSubscribeEndpoints: List[OnsubscribeendpointsItem]
    onUnsubscribeEndpoints: List[Serviceendpoint4]


class Subscribebutton(TypedDict):
    subscribeButtonRenderer: Subscribebuttonrenderer


class Visittracking(TypedDict):
    remarketingPing: str


class Subscribercounttext(TypedDict):
    accessibility: Accessibilitydata
    simpleText: str


class Channeltaglinerenderer(TypedDict):
    content: str
    maxLines: int
    moreLabel: str
    moreEndpoint: Endpoint
    moreIcon: Icon


class Tagline(TypedDict):
    channelTaglineRenderer: Channeltaglinerenderer


class C4tabbedheaderrenderer(TypedDict):
    channelId: str
    title: str
    navigationEndpoint: Navigationendpoint
    avatar: Avatar
    banner: Avatar
    badges: List[BadgesItem]
    headerLinks: Headerlinks
    subscribeButton: Subscribebutton
    visitTracking: Visittracking
    subscriberCountText: Subscribercounttext
    tvBanner: Avatar
    mobileBanner: Avatar
    trackingParams: str
    channelHandleText: Joineddatetext
    style: str
    videosCountText: Joineddatetext
    tagline: Tagline


class Header(TypedDict):
    c4TabbedHeaderRenderer: C4tabbedheaderrenderer


class Channelmetadatarenderer(TypedDict):
    title: str
    description: str
    rssUrl: str
    channelConversionUrl: str
    externalId: str
    keywords: str
    ownerUrls: List[str]
    avatar: Avatar
    channelUrl: str
    isFamilySafe: bool
    availableCountryCodes: List[str]
    androidDeepLink: str
    androidAppindexingLink: str
    iosAppindexingLink: str
    vanityChannelUrl: str


class Metadata(TypedDict):
    channelMetadataRenderer: Channelmetadatarenderer


class Browseendpoint1(TypedDict):
    browseId: str


class Endpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint1


class Topbarlogorenderer(TypedDict):
    iconImage: Icon
    tooltipText: Joineddatetext
    endpoint: Endpoint0
    trackingParams: str
    overrideEntityKey: str


class Logo(TypedDict):
    topbarLogoRenderer: Topbarlogorenderer


class Websearchboxconfig(TypedDict):
    requestLanguage: str
    requestDomain: str
    hasOnscreenKeyboard: bool
    focusSearchbox: bool


class Config(TypedDict):
    webSearchboxConfig: Websearchboxconfig


class Searchendpoint(TypedDict):
    query: str


class Searchendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    searchEndpoint: Searchendpoint


class Buttonrenderer6(TypedDict):
    style: str
    size: str
    isDisabled: bool
    icon: Icon
    trackingParams: str
    accessibilityData: Accessibilitydata


class Clearbutton(TypedDict):
    buttonRenderer: Buttonrenderer6


class Fusionsearchboxrenderer(TypedDict):
    icon: Icon
    placeholderText: Joineddatetext
    config: Config
    trackingParams: str
    searchEndpoint: Searchendpoint0
    clearButton: Clearbutton


class Searchbox(TypedDict):
    fusionSearchboxRenderer: Fusionsearchboxrenderer


class Uploadendpoint(TypedDict):
    hack: bool


class Navigationendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    uploadEndpoint: Uploadendpoint


class Compactlinkrenderer(TypedDict):
    icon: Icon
    title: Joineddatetext
    navigationEndpoint: Navigationendpoint0
    trackingParams: str
    style: str


class ItemsItem6(TypedDict):
    compactLinkRenderer: Compactlinkrenderer


class Signalnavigationendpoint(TypedDict):
    signal: str


class Navigationendpoint1(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    signalNavigationEndpoint: Signalnavigationendpoint


class Compactlinkrenderer0(TypedDict):
    icon: Icon
    title: Joineddatetext
    navigationEndpoint: Navigationendpoint1
    trackingParams: str
    style: str


class ItemsItem7(TypedDict):
    compactLinkRenderer: Compactlinkrenderer0


class Browseendpoint2(TypedDict):
    browseId: str
    params: str


class Navigationendpoint2(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint2


class Compactlinkrenderer1(TypedDict):
    icon: Icon
    title: Joineddatetext
    navigationEndpoint: Navigationendpoint2
    trackingParams: str
    style: str


class ItemsItem8(TypedDict):
    compactLinkRenderer: Compactlinkrenderer1


class Multipagemenusectionrenderer(TypedDict):
    items: List[Union[ItemsItem8, ItemsItem6, ItemsItem7]]
    trackingParams: str


class SectionsItem(TypedDict):
    multiPageMenuSectionRenderer: Multipagemenusectionrenderer


class Multipagemenurenderer0(TypedDict):
    sections: List[SectionsItem]
    trackingParams: str
    style: str


class Menurenderer(TypedDict):
    multiPageMenuRenderer: Multipagemenurenderer0


class Topbarmenubuttonrenderer(TypedDict):
    icon: Icon
    menuRenderer: Menurenderer
    trackingParams: str
    accessibility: Accessibilitydata
    tooltip: str
    style: str


class TopbarbuttonsItem(TypedDict):
    topbarMenuButtonRenderer: Topbarmenubuttonrenderer


class Openpopupaction7(TypedDict):
    popup: Popup0
    popupType: str
    beReused: bool


class ActionsItem4(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction7


class Signalserviceendpoint4(TypedDict):
    signal: str
    actions: List[ActionsItem4]


class Menurequest(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    signalServiceEndpoint: Signalserviceendpoint4


class Updateunseencountendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    signalServiceEndpoint: Signalnavigationendpoint


class Notificationtopbarbuttonrenderer(TypedDict):
    icon: Icon
    menuRequest: Menurequest
    style: str
    trackingParams: str
    accessibility: Accessibilitydata
    tooltip: str
    updateUnseenCountEndpoint: Updateunseencountendpoint
    notificationCount: int
    handlerDatas: List[str]


class TopbarbuttonsItem0(TypedDict):
    notificationTopbarButtonRenderer: Notificationtopbarbuttonrenderer


class Avatar0(TypedDict):
    thumbnails: List[ThumbnailsItem]
    accessibility: Accessibilitydata


class Topbarmenubuttonrenderer0(TypedDict):
    avatar: Avatar0
    menuRequest: Menurequest
    trackingParams: str
    accessibility: Accessibilitydata
    tooltip: str


class TopbarbuttonsItem1(TypedDict):
    topbarMenuButtonRenderer: Topbarmenubuttonrenderer0


class Hotkeydialogsectionoptionrenderer(TypedDict):
    label: Joineddatetext
    hotkey: str


class OptionsItem(TypedDict):
    hotkeyDialogSectionOptionRenderer: Hotkeydialogsectionoptionrenderer


class Hotkeydialogsectionoptionrenderer0(TypedDict):
    label: Joineddatetext
    hotkey: str
    hotkeyAccessibilityLabel: Accessibilitydata


class OptionsItem0(TypedDict):
    hotkeyDialogSectionOptionRenderer: Hotkeydialogsectionoptionrenderer0


class Hotkeydialogsectionrenderer(TypedDict):
    title: Joineddatetext
    options: List[Union[OptionsItem, OptionsItem0]]


class SectionsItem0(TypedDict):
    hotkeyDialogSectionRenderer: Hotkeydialogsectionrenderer


class Hotkeydialogsectionrenderer0(TypedDict):
    title: Joineddatetext
    options: List[OptionsItem]


class SectionsItem1(TypedDict):
    hotkeyDialogSectionRenderer: Hotkeydialogsectionrenderer0


class Buttonrenderer7(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Joineddatetext
    trackingParams: str


class Dismissbutton(TypedDict):
    buttonRenderer: Buttonrenderer7


class Hotkeydialogrenderer(TypedDict):
    title: Joineddatetext
    sections: List[Union[SectionsItem0, SectionsItem1]]
    dismissButton: Dismissbutton
    trackingParams: str


class Hotkeydialog(TypedDict):
    hotkeyDialogRenderer: Hotkeydialogrenderer


class ActionsItem5(TypedDict):
    clickTrackingParams: str
    signalAction: Signalnavigationendpoint


class Signalserviceendpoint5(TypedDict):
    signal: str
    actions: List[ActionsItem5]


class Command4(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint5


class Buttonrenderer8(TypedDict):
    trackingParams: str
    command: Command4


class Backbutton(TypedDict):
    buttonRenderer: Buttonrenderer8


class Buttonrenderer9(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Joineddatetext
    trackingParams: str
    command: Command4


class A11yskipnavigationbutton(TypedDict):
    buttonRenderer: Buttonrenderer9


class Voicesearchdialogrenderer(TypedDict):
    placeholderHeader: Joineddatetext
    promptHeader: Joineddatetext
    exampleQuery1: Joineddatetext
    exampleQuery2: Joineddatetext
    promptMicrophoneLabel: Joineddatetext
    loadingHeader: Joineddatetext
    connectionErrorHeader: Joineddatetext
    connectionErrorMicrophoneLabel: Joineddatetext
    permissionsHeader: Joineddatetext
    permissionsSubtext: Joineddatetext
    disabledHeader: Joineddatetext
    disabledSubtext: Joineddatetext
    microphoneButtonAriaLabel: Joineddatetext
    exitButton: Clearbutton
    trackingParams: str
    microphoneOffPromptHeader: Joineddatetext


class Popup7(TypedDict):
    voiceSearchDialogRenderer: Voicesearchdialogrenderer


class Openpopupaction8(TypedDict):
    popup: Popup7
    popupType: str


class ActionsItem6(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction8


class Signalserviceendpoint6(TypedDict):
    signal: str
    actions: List[ActionsItem6]


class Serviceendpoint5(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint6


class Buttonrenderer10(TypedDict):
    style: str
    size: str
    isDisabled: bool
    serviceEndpoint: Serviceendpoint5
    icon: Icon
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibilitydata


class Voicesearchbutton(TypedDict):
    buttonRenderer: Buttonrenderer10


class Desktoptopbarrenderer(TypedDict):
    logo: Logo
    searchbox: Searchbox
    trackingParams: str
    countryCode: str
    topbarButtons: List[
        Union[TopbarbuttonsItem0, TopbarbuttonsItem1, TopbarbuttonsItem]
    ]
    hotkeyDialog: Hotkeydialog
    backButton: Backbutton
    forwardButton: Backbutton
    a11ySkipNavigationButton: A11yskipnavigationbutton
    voiceSearchButton: Voicesearchbutton


class Topbar(TypedDict):
    desktopTopbarRenderer: Desktoptopbarrenderer


class LinkalternatesItem(TypedDict):
    hrefUrl: str


class Microformatdatarenderer(TypedDict):
    urlCanonical: str
    title: str
    description: str
    thumbnail: Avatar
    siteName: str
    appName: str
    androidPackage: str
    iosAppStoreId: str
    iosAppArguments: str
    ogType: str
    urlApplinksWeb: str
    urlApplinksIos: str
    urlApplinksAndroid: str
    urlTwitterIos: str
    urlTwitterAndroid: str
    twitterCardType: str
    twitterSiteHandle: str
    schemaDotOrgType: str
    noindex: bool
    unlisted: bool
    familySafe: bool
    tags: List[str]
    availableCountries: List[str]
    linkAlternates: List[LinkalternatesItem]


class Microformat(TypedDict):
    microformatDataRenderer: Microformatdatarenderer


class Subscriptionstateentity(TypedDict):
    key: str
    subscribed: bool


class Payload(TypedDict):
    subscriptionStateEntity: Subscriptionstateentity


class MutationsItem(TypedDict):
    entityKey: str
    type: str
    payload: Payload


class Timestamp(TypedDict):
    seconds: str
    nanos: int


class Entitybatchupdate(TypedDict):
    mutations: List[MutationsItem]
    timestamp: Timestamp


class Frameworkupdates(TypedDict):
    entityBatchUpdate: Entitybatchupdate


class Root(TypedDict):
    responseContext: Responsecontext
    contents: Contents
    header: Header
    metadata: Metadata
    trackingParams: str
    topbar: Topbar
    microformat: Microformat
    frameworkUpdates: Frameworkupdates
