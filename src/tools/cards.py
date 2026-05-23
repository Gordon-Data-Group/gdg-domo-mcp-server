"""Cards tools — KPI/chart cards, sharing, drill paths, problems.

API reference: api-definitions-md/11-cards.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def cards_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: count (int), offset (int), query (str, use '*' for all), "
            "combineResults (bool), filters (list of filter objects with name, field, facetType, "
            "value, filterType, count, displayValue), "
            "sort ({fieldSorts: [{enum, field, sortOrder, label, order}]}), "
            "facetValuesToInclude (list), facetValueLimit (int), facetValueOffset (int), "
            "includePhonetic (bool), queryProfile (str e.g. 'GLOBAL'), state (str), "
            "topic, savedSearchId, entityList (e.g. [['card']])"
        ),
    ],
) -> Any:
    """Search cards using the global search API."""
    return auth.post("/search/v1/query", body=body)


@mcp.tool()
def cards_list_admin_summary(
    body: Annotated[
        dict[str, Any],
        (
            "Filter/sort body. Keys: ascending (bool), orderBy (str e.g. 'cardTitle'), "
            "includeCardTypeClause (bool), cardTypes (list e.g. ['kpi','badge']), "
            "includeCardOwnerClause (bool), addCardWithNoOwner (bool), "
            "cardOwners (list of {id: int, type: str}), "
            "includeCardTitleClause (bool), cardTitleSearchText (str), "
            "includePageTitleClause (bool), notOnPage (bool), pageIds (list of int), "
            "includeLastModifiedDateClause (bool), lastModifiedDateOperand (str), "
            "lastModifiedStartDate (str YYYY-MM-DD), lastModifiedEndDate (str YYYY-MM-DD)"
        ),
    ],
    limit: Annotated[int | None, "Max cards to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List cards with admin-level metadata using flexible filters."""
    return auth.post("/content/v2/cards/adminsummary", body=body, limit=limit, skip=skip)


@mcp.tool()
def cards_get(
    urns: Annotated[str, "Comma-separated card URNs (numeric IDs) to fetch"],
    parts: Annotated[str | None, "Comma-separated parts to include in the response"] = None,
    include_filtered: Annotated[bool | None, "Include filtered/hidden cards"] = None,
) -> Any:
    """Get one or more cards by URN."""
    return auth.get("/content/v1/cards", urns=urns, parts=parts, includeFiltered=include_filtered)


@mcp.tool()
def cards_get_notebook(
    card_id: Annotated[str, "Notebook card ID"],
) -> Any:
    """Get a notebook card by ID."""
    return auth.get(f"/content/v1/cards/notebook/{card_id}")


@mcp.tool()
def cards_get_linked(
    card_id: Annotated[str, "Card ID"],
) -> Any:
    """Get cards linked to a given card."""
    return auth.get(f"/content/v1/cards/{card_id}/link")


@mcp.tool()
def cards_get_view_counts(
    urns: Annotated[list[int], "List of card URNs (numeric) to get view counts for"],
) -> Any:
    """Get view counts for one or more cards."""
    return auth.put("/content/v1/analytics/views/cards/counts", body={"urns": urns})


@mcp.tool()
def cards_get_access(
    card_id: Annotated[str, "Card ID"],
    expand_users: Annotated[bool | None, "Expand group entries to show individual users"] = None,
) -> Any:
    """Get the access list for a card."""
    return auth.get(f"/content/v1/share/accesslist/badge/{card_id}", expandUsers=expand_users)


@mcp.tool()
def cards_get_dataset_schema(
    card_id: Annotated[str, "Card ID"],
) -> Any:
    """Get the dataset schema details for a card."""
    return auth.get(f"/content/v1/cards/{card_id}/details")


@mcp.tool()
def cards_get_by_dataset(
    dataset_id: Annotated[str, "Dataset ID"],
    drill: Annotated[bool | None, "Include drill-path cards"] = None,
) -> Any:
    """Get all cards powered by a given dataset."""
    return auth.get(f"/content/v1/datasources/{dataset_id}/cards", drill=drill)


@mcp.tool()
def cards_get_min_max_dates(
    urns: Annotated[str, "Comma-separated card URNs to query"],
) -> Any:
    """Get the min and max date values across one or more cards."""
    return auth.get("/content/v1/cards/minmaxdates", urns=urns)


@mcp.tool()
def cards_get_user_accessible(
    user_id: Annotated[str, "User ID"],
    limit: Annotated[int | None, "Max cards to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Get cards that a specific user has access to."""
    return auth.get(f"/content/v1/access/users/{user_id}/cards", limit=limit, offset=offset)


@mcp.tool()
def cards_get_chart_type_options(
    chart_type: Annotated[str, "Chart type identifier (e.g. 'badge_basic_table')"],
) -> Any:
    """Get available configuration options for a chart type."""
    return auth.get(f"/content/v1/cards/kpi/{chart_type}/options")


@mcp.tool()
def cards_get_color_palette() -> Any:
    """Get the global color palette available for card styling."""
    return auth.get("/content/v1/cards/kpi/palette")


@mcp.tool()
def cards_validate_dataset_move(
    card_id: Annotated[str, "Card ID to validate"],
    dataset_id: Annotated[str, "Target dataset ID to move the card to"],
) -> Any:
    """Validate whether a card can be moved to a different dataset."""
    return auth.get(f"/content/v1/cards/kpi/{card_id}/comparemove/{dataset_id}")


@mcp.tool()
def cards_get_definition_for_update(
    urn: Annotated[str, "Card URN"],
    dynamic_text: Annotated[bool | None, "Include dynamic text definitions"] = None,
    variables: Annotated[bool | None, "Include variable definitions"] = None,
) -> Any:
    """Get a card's full definition. Returns an array where result[0] contains:
    - subscriptions: LIST of objects with {cardId, dataSourceId, componentName, subscription: {...}}
    - metadataOverrides.components: LIST of {component, chartType, overrides, goal}

    To build a cards_update body from this response:
      1. Convert subscriptions list → dict keyed by componentName using the inner 'subscription'
         object, then REMOVE 'dataSourceId' from each subscription (it belongs only in dataProvider)
      2. Convert metadataOverrides.components list → 'charts' dict keyed by 'component' field
      3. Wrap in {definition: {subscriptions, charts, formulas, annotations, conditionalFormats,
         controls, segments, dynamicTitle, dynamicDescription, chartVersion, allowTableDrill,
         inputTable, modified, title, description}, dataProvider: {dataSourceId}, variables}

    To build a cards_create body: same as above but KEEP 'dataSourceId' inside each subscription.
    """
    body: dict[str, Any] = {"urn": urn}
    if dynamic_text is not None:
        body["dynamicText"] = dynamic_text
    if variables is not None:
        body["variables"] = variables
    return auth.put("/content/v3/cards/kpi/definition", body=body)


@mcp.tool()
def cards_render(
    card_id: Annotated[str, "Card ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Render options. Keys: queryOverrides (dict), "
            "packet ({textColor, scaleLineColor, pageLayout (bool), transparent (bool), cardLinking (bool)}), "
            "imageMap (bool), pageLayout (null or str), width (int), height (int), scale (float), "
            "cardLoadContext ({context, sessionId, visibilityState, contextId, trigger})"
        ),
    ],
    parts: Annotated[str | None, "Comma-separated parts: e.g. 'summary,graph,annotations'"] = None,
) -> Any:
    """Render a card and return its data/image payload."""
    return auth.put(f"/content/v1/cards/kpi/{card_id}/render", body=body, parts=parts)


@mcp.tool()
def cards_create(
    body: Annotated[
        dict[str, Any],
        (
            "Card creation body. Shape: {definition, dataProvider, variables?}. "
            "definition.subscriptions is a DICT keyed by component name (e.g. 'main', 'big_number'). "
            "Each subscription object MUST include 'dataSourceId' directly alongside its other fields "
            "(name, columns, filters, orderBy, groupBy, fiscal, projection, distinct, etc.). "
            "definition.charts is a DICT keyed by component name: "
            "{main: {component, chartType, overrides, goal}}. "
            "Other definition keys: formulas {dsUpdated,dsDeleted,card}, annotations {new,modified,deleted}, "
            "conditionalFormats {card,datasource}, controls, segments {active,create,update,delete}, "
            "dynamicTitle {text:[{type,text}]}, dynamicDescription {text,displayOnCardDetails}, "
            "chartVersion, allowTableDrill, inputTable, modified (epoch ms), title, description. "
            "dataProvider: {dataSourceId: str}. "
            "NOTE: dataSourceId must appear BOTH in dataProvider AND inside every subscription object. "
            "Available chartType values for definition.charts[component].chartType — "
            "Bar/Column (vertical): badge_vert_bar, badge_vert_multibar, badge_vert_stackedbar, "
            "badge_vert_percentbar, badge_vert_nestedbar, badge_vert_dual_stackedbar, "
            "badge_vert_facetedbar, badge_vert_histogram, badge_vert_marimekko, badge_vert_rtbar, "
            "badge_vert_rtmultibar, badge_vert_rtstackedbar, badge_vert_waterfall, badge_vert_bullet. "
            "Bar (horizontal): badge_horiz_bar, badge_horiz_multibar, badge_horiz_stackedbar, "
            "badge_horiz_percentbar, badge_horiz_nestedbar, badge_horiz_dual_stackedbar, "
            "badge_horiz_facetedbar, badge_horiz_histogram, badge_horiz_marimekko, badge_horiz_rtbar, "
            "badge_horiz_rtmultibar, badge_horiz_rtstackedbar, badge_horiz_waterfall, badge_horiz_bullet. "
            "Line: badge_trendline, badge_two_trendline, badge_curvedline, badge_stepline, "
            "badge_symbolline, badge_curved_symbolline, badge_rttrendline, badge_curved_rttrendline, "
            "badge_horiz_trendline, badge_horiz_curvedline, badge_horiz_stepline, badge_horiz_symbolline, "
            "badge_horiz_curved_symbolline, badge_curved_rt_symbolline, badge_curved_rttrendline, "
            "badge_variance_line, badge_xy_line, badge_spark_line, badge_slope. "
            "Combo (bar+line): badge_line_bar, badge_line_clusterbar, badge_line_stackedbar, "
            "badge_vert_bar_line, badge_vert_bar_overlay, badge_horiz_bar_line, badge_horiz_bar_overlay, "
            "badge_curved_line_bar, badge_curved_line_stackedbar, badge_horiz_line_bar, "
            "badge_horiz_line_clusterbar, badge_horiz_line_stackedbar, badge_vert_nested_linebar, "
            "badge_horiz_nested_linebar. "
            "Area: badge_stream, badge_stackedtrend, badge_horiz_stackedtrend, badge_vert_area_overlay, "
            "badge_horiz_area_overlay, badge_vert_curved_stacked_area, badge_horiz_curved_stacked_area, "
            "badge_vert_step_area_overlay, badge_horiz_step_area_overlay, badge_vert_curved_area_overlay, "
            "badge_horiz_curved_area_overlay. "
            "Scatter/Bubble/Dot: badge_xyscatterplot, badge_xyscatterplot_basic, badge_xybubble, "
            "badge_bubble, badge_packed_bubble, badge_category_scatter, badge_symbol_bar, "
            "badge_symbol_stackedbar, badge_horiz_symbol, badge_horiz_symbol_bar, "
            "badge_horiz_symbol_stackedbar, badge_horiz_symbol_overlay, badge_vert_symbol, "
            "badge_vert_symbol_overlay, badge_vert_dotplot_overlay, badge_horiz_dotplot_overlay, "
            "badge_vert_multi_dotplot, badge_horiz_multi_dotplot, badge_vert_stacked_dotplot, "
            "badge_horiz_stacked_dotplot, badge_vert_line_multi_dotplot, badge_horiz_line_multi_dotplot, "
            "badge_vert_line_stacked_dotplot, badge_horiz_line_stacked_dotplot. "
            "Pie/Donut/Circular: badge_pie, badge_donut, badge_nautilus, badge_nautilus_donut, "
            "badge_nightingale_rose, badge_sunburst, badge_waffle, badge_radar, badge_sankey, "
            "badge_sankey_path, badge_sankey_circular, badge_stream_funnel. "
            "Funnel: badge_funnel, badge_funnel_bars, badge_funnel_swing. "
            "Gauges/Progress: badge_gauge, badge_filledgauge, badge_compfillgauge_basic, "
            "badge_compfillgauge_adv, badge_facegauge, badge_imagegauge, badge_shapegauge, "
            "badge_compgauge, badge_in_range_gauge, badge_radial_progress, badge_multi_radial_progress, "
            "badge_progressbar, badge_bullet, badge_horiz_boxplot, badge_vert_boxplot. "
            "Single Value/KPI: badge_singlevalue, badge_multi_value, badge_multi_value_cols, "
            "badge_summary_comparison, badge_summary_num_text, badge_summary_time_comparison, "
            "badge_spark_bar, badge_highlow, badge_horiz_highlow, badge_pareto, badge_bump, "
            "badge_stock_candlestick, badge_risk_heatmap. "
            "Period-over-Period: badge_pop_trendline, badge_pop_trendline_var, badge_pop_bar_line, "
            "badge_pop_bar_line_var, badge_pop_line_bar, badge_pop_line_bar_var, badge_pop_multi_value, "
            "badge_pop_vert_multibar, badge_pop_filledgauge, badge_pop_progressbar, badge_pop_rttrendline, "
            "badge_pop_shapegauge, badge_pop_table, badge_pop_flex_table, badge_pop_trendline_play, "
            "badge_pop_vert_bar_play, badge_pop_pie_play, badge_pop_donut_play. "
            "Tables: badge_table, badge_basic_table, badge_flex_table, badge_pivot_table, "
            "badge_heatmap_table. "
            "Maps: badge_world_map, badge_world, badge_map, badge_map_us_state, badge_map_us_county, "
            "badge_map_latlong, badge_map_latlong_route, badge_map_custom, badge_map_africa, "
            "badge_map_asia, badge_map_australia, badge_map_austria, badge_map_brazil, badge_map_canada, "
            "badge_map_chile, badge_map_china, badge_map_europe, badge_map_france, "
            "badge_map_france_dept, badge_map_germany, badge_map_ghana, badge_map_india, "
            "badge_map_indonesia, badge_map_italy, badge_map_japan, badge_map_malaysia, "
            "badge_map_mexico, badge_map_middle_east, badge_map_new_zealand, badge_map_nigeria, "
            "badge_map_north_america, badge_map_panama, badge_map_peru, badge_map_philippines, "
            "badge_map_portugal, badge_map_south_america, badge_map_south_korea, badge_map_spain, "
            "badge_map_switzerland, badge_map_uae, badge_map_uk_area, badge_map_uk_postal, "
            "badge_map_united_kingdom. "
            "Heatmap/Calendar/Gantt: badge_heatmap, badge_calendar, badge_calendar_entry, "
            "badge_category_calendar, badge_gantt, badge_gantt_dep, badge_gantt_percent, "
            "badge_treemap, badge_word_cloud. "
            "Data Science: badge_ds_forecasting, badge_ds_outliers, badge_ds_pred_modeling, "
            "badge_ds_spc, badge_ds_percentile, badge_ds_percentile_dist, badge_confusion_matrix, "
            "badge_correlation_matrix. "
            "Selectors/Filters: badge_slicer, badge_dropdown_selector, badge_checkbox_selector, "
            "badge_radio_selector, badge_date_selector, badge_range_selector, badge_slider_selector, "
            "badge_buttons. "
            "Text/Content: badge_textbox, badge_dynamic_textbox, badge_text_entry."
        ),
    ],
    page_id: Annotated[str | None, "Page ID to add the card to after creation"] = None,
    parent_urn: Annotated[str | None, "Parent card URN for drill-path cards"] = None,
) -> Any:
    """Create a new KPI card.

    Key difference from cards_update: each subscription in definition.subscriptions must contain
    'dataSourceId'. When converting a cards_get_definition_for_update response, keep 'dataSourceId'
    inside each subscription object.
    """
    return auth.put("/content/v3/cards/kpi", body=body, pageId=page_id, parentUrn=parent_urn)


@mcp.tool()
def cards_share_access(
    resources: Annotated[
        list[dict[str, Any]],
        "List of cards to share, each with 'type' ('badge') and 'id' (str card URN)",
    ],
    recipients: Annotated[
        list[dict[str, Any]],
        "List of recipients, each with 'type' ('user' or 'group', lowercase) and 'id' (str)",
    ],
    message: Annotated[str | None, "Optional message to include with the share notification"] = None,
    send_email: Annotated[bool | None, "Send an email notification to recipients"] = None,
) -> Any:
    """Share one or more cards with users or groups."""
    body: dict[str, Any] = {"resources": resources, "recipients": recipients}
    if message is not None:
        body["message"] = message
    return auth.post("/content/v1/share", body=body, sendEmail=send_email)


@mcp.tool()
def cards_create_history_entry(
    card_id: Annotated[str, "Card ID"],
    changes: Annotated[
        dict[str, Any],
        (
            "Change summary. Keys: kpi (object with bool flags: title, description, "
            "aggregationChanged, dimensionsChanged, orderingChanged, filtersChanged), "
            "data (dict), initial (bool)"
        ),
    ],
    comment: Annotated[str | None, "Human-readable comment describing the change"] = None,
) -> Any:
    """Add a change entry to a card's history."""
    body: dict[str, Any] = {"changes": changes}
    if comment is not None:
        body["comment"] = comment
    return auth.post(f"/kpis/{card_id}/history", body=body)


@mcp.tool()
def cards_update(
    card_id: Annotated[str, "Card ID to update"],
    body: Annotated[
        dict[str, Any],
        (
            "Full card definition to replace. Shape: {definition, dataProvider, variables?}. "
            "definition.subscriptions is a DICT keyed by component name (e.g. 'main', 'big_number'). "
            "Each subscription object must NOT contain 'dataSourceId' — that belongs only in "
            "dataProvider.dataSourceId at the top level. "
            "Subscription fields: name, columns, filters, orderBy, groupBy, fiscal, projection, "
            "distinct, limit (big_number only), dateGrain (main only). "
            "definition.charts is a DICT keyed by component name: "
            "{main: {component, chartType, overrides, goal}}. "
            "Other definition keys: formulas {dsUpdated,dsDeleted,card}, annotations {new,modified,deleted}, "
            "conditionalFormats {card,datasource}, controls, segments {active,create,update,delete}, "
            "dynamicTitle {text:[{type,text}]}, dynamicDescription {text,displayOnCardDetails}, "
            "chartVersion, allowTableDrill, inputTable, modified (epoch ms), title, description. "
            "dataProvider: {dataSourceId: str}. "
            "NOTE: dataSourceId must appear ONLY in dataProvider, not inside subscriptions. "
            "Available chartType values for definition.charts[component].chartType — "
            "Bar/Column (vertical): badge_vert_bar, badge_vert_multibar, badge_vert_stackedbar, "
            "badge_vert_percentbar, badge_vert_nestedbar, badge_vert_dual_stackedbar, "
            "badge_vert_facetedbar, badge_vert_histogram, badge_vert_marimekko, badge_vert_rtbar, "
            "badge_vert_rtmultibar, badge_vert_rtstackedbar, badge_vert_waterfall, badge_vert_bullet. "
            "Bar (horizontal): badge_horiz_bar, badge_horiz_multibar, badge_horiz_stackedbar, "
            "badge_horiz_percentbar, badge_horiz_nestedbar, badge_horiz_dual_stackedbar, "
            "badge_horiz_facetedbar, badge_horiz_histogram, badge_horiz_marimekko, badge_horiz_rtbar, "
            "badge_horiz_rtmultibar, badge_horiz_rtstackedbar, badge_horiz_waterfall, badge_horiz_bullet. "
            "Line: badge_trendline, badge_two_trendline, badge_curvedline, badge_stepline, "
            "badge_symbolline, badge_curved_symbolline, badge_rttrendline, badge_curved_rttrendline, "
            "badge_horiz_trendline, badge_horiz_curvedline, badge_horiz_stepline, badge_horiz_symbolline, "
            "badge_horiz_curved_symbolline, badge_curved_rt_symbolline, badge_curved_rttrendline, "
            "badge_variance_line, badge_xy_line, badge_spark_line, badge_slope. "
            "Combo (bar+line): badge_line_bar, badge_line_clusterbar, badge_line_stackedbar, "
            "badge_vert_bar_line, badge_vert_bar_overlay, badge_horiz_bar_line, badge_horiz_bar_overlay, "
            "badge_curved_line_bar, badge_curved_line_stackedbar, badge_horiz_line_bar, "
            "badge_horiz_line_clusterbar, badge_horiz_line_stackedbar, badge_vert_nested_linebar, "
            "badge_horiz_nested_linebar. "
            "Area: badge_stream, badge_stackedtrend, badge_horiz_stackedtrend, badge_vert_area_overlay, "
            "badge_horiz_area_overlay, badge_vert_curved_stacked_area, badge_horiz_curved_stacked_area, "
            "badge_vert_step_area_overlay, badge_horiz_step_area_overlay, badge_vert_curved_area_overlay, "
            "badge_horiz_curved_area_overlay. "
            "Scatter/Bubble/Dot: badge_xyscatterplot, badge_xyscatterplot_basic, badge_xybubble, "
            "badge_bubble, badge_packed_bubble, badge_category_scatter, badge_symbol_bar, "
            "badge_symbol_stackedbar, badge_horiz_symbol, badge_horiz_symbol_bar, "
            "badge_horiz_symbol_stackedbar, badge_horiz_symbol_overlay, badge_vert_symbol, "
            "badge_vert_symbol_overlay, badge_vert_dotplot_overlay, badge_horiz_dotplot_overlay, "
            "badge_vert_multi_dotplot, badge_horiz_multi_dotplot, badge_vert_stacked_dotplot, "
            "badge_horiz_stacked_dotplot, badge_vert_line_multi_dotplot, badge_horiz_line_multi_dotplot, "
            "badge_vert_line_stacked_dotplot, badge_horiz_line_stacked_dotplot. "
            "Pie/Donut/Circular: badge_pie, badge_donut, badge_nautilus, badge_nautilus_donut, "
            "badge_nightingale_rose, badge_sunburst, badge_waffle, badge_radar, badge_sankey, "
            "badge_sankey_path, badge_sankey_circular, badge_stream_funnel. "
            "Funnel: badge_funnel, badge_funnel_bars, badge_funnel_swing. "
            "Gauges/Progress: badge_gauge, badge_filledgauge, badge_compfillgauge_basic, "
            "badge_compfillgauge_adv, badge_facegauge, badge_imagegauge, badge_shapegauge, "
            "badge_compgauge, badge_in_range_gauge, badge_radial_progress, badge_multi_radial_progress, "
            "badge_progressbar, badge_bullet, badge_horiz_boxplot, badge_vert_boxplot. "
            "Single Value/KPI: badge_singlevalue, badge_multi_value, badge_multi_value_cols, "
            "badge_summary_comparison, badge_summary_num_text, badge_summary_time_comparison, "
            "badge_spark_bar, badge_highlow, badge_horiz_highlow, badge_pareto, badge_bump, "
            "badge_stock_candlestick, badge_risk_heatmap. "
            "Period-over-Period: badge_pop_trendline, badge_pop_trendline_var, badge_pop_bar_line, "
            "badge_pop_bar_line_var, badge_pop_line_bar, badge_pop_line_bar_var, badge_pop_multi_value, "
            "badge_pop_vert_multibar, badge_pop_filledgauge, badge_pop_progressbar, badge_pop_rttrendline, "
            "badge_pop_shapegauge, badge_pop_table, badge_pop_flex_table, badge_pop_trendline_play, "
            "badge_pop_vert_bar_play, badge_pop_pie_play, badge_pop_donut_play. "
            "Tables: badge_table, badge_basic_table, badge_flex_table, badge_pivot_table, "
            "badge_heatmap_table. "
            "Maps: badge_world_map, badge_world, badge_map, badge_map_us_state, badge_map_us_county, "
            "badge_map_latlong, badge_map_latlong_route, badge_map_custom, badge_map_africa, "
            "badge_map_asia, badge_map_australia, badge_map_austria, badge_map_brazil, badge_map_canada, "
            "badge_map_chile, badge_map_china, badge_map_europe, badge_map_france, "
            "badge_map_france_dept, badge_map_germany, badge_map_ghana, badge_map_india, "
            "badge_map_indonesia, badge_map_italy, badge_map_japan, badge_map_malaysia, "
            "badge_map_mexico, badge_map_middle_east, badge_map_new_zealand, badge_map_nigeria, "
            "badge_map_north_america, badge_map_panama, badge_map_peru, badge_map_philippines, "
            "badge_map_portugal, badge_map_south_america, badge_map_south_korea, badge_map_spain, "
            "badge_map_switzerland, badge_map_uae, badge_map_uk_area, badge_map_uk_postal, "
            "badge_map_united_kingdom. "
            "Heatmap/Calendar/Gantt: badge_heatmap, badge_calendar, badge_calendar_entry, "
            "badge_category_calendar, badge_gantt, badge_gantt_dep, badge_gantt_percent, "
            "badge_treemap, badge_word_cloud. "
            "Data Science: badge_ds_forecasting, badge_ds_outliers, badge_ds_pred_modeling, "
            "badge_ds_spc, badge_ds_percentile, badge_ds_percentile_dist, badge_confusion_matrix, "
            "badge_correlation_matrix. "
            "Selectors/Filters: badge_slicer, badge_dropdown_selector, badge_checkbox_selector, "
            "badge_radio_selector, badge_date_selector, badge_range_selector, badge_slider_selector, "
            "badge_buttons. "
            "Text/Content: badge_textbox, badge_dynamic_textbox, badge_text_entry."
        ),
    ],
) -> Any:
    """Replace a card's full definition.

    Key difference from cards_create: subscription objects in definition.subscriptions must NOT
    contain 'dataSourceId'. When converting a cards_get_definition_for_update response, strip
    'dataSourceId' from each inner subscription object before submitting.
    """
    return auth.put(f"/content/v3/cards/kpi/{card_id}", body=body)


@mcp.tool()
def cards_lock_unlock(
    card_id: Annotated[str, "Card ID"],
    locked: Annotated[bool, "True to lock the card, False to unlock it"],
) -> Any:
    """Lock or unlock a card."""
    return auth.put(f"/content/v1/cards/{card_id}", body={"locked": locked})


@mcp.tool()
def cards_bulk_add_to_pages(
    card_ids: Annotated[list[str], "List of card IDs to add"],
    destination_page_ids: Annotated[list[int], "List of page IDs to add the cards to"],
) -> Any:
    """Add multiple cards to pages without removing them from existing pages."""
    return auth.put(
        "/content/v1/cards/bulk/pages",
        body={"cardIds": card_ids, "destinationPageIds": destination_page_ids},
    )


@mcp.tool()
def cards_move_to_pages(
    card_id: Annotated[str, "Card ID to move"],
    page_ids: Annotated[list[int], "List of page IDs the card should belong to (replaces current pages)"],
) -> Any:
    """Set the pages a card belongs to, replacing its current page assignments."""
    return auth.put(f"/content/v1/cards/{card_id}/pages", body=page_ids)


@mcp.tool()
def cards_increment_views(
    urns: Annotated[list[str], "List of card URN strings to record views for"],
    context: Annotated[str, "View context ('AUTHENTICATED' or 'EMBEDDED')"] = "AUTHENTICATED",
) -> Any:
    """Increment view counters for one or more cards."""
    return auth.put("/content/v1/analytics/views/cards/increment", body={"urns": urns, "context": context})


@mcp.tool()
def cards_update_owners(
    action: Annotated[str, "Ownership action: 'add' or 'remove'"],
    card_ids: Annotated[list[int], "List of card IDs to update"],
    card_owners: Annotated[
        list[dict[str, Any]],
        "List of owners, each with 'id' (str) and 'type' (e.g. 'USER')",
    ],
) -> Any:
    """Add or remove owners from cards."""
    return auth.post(
        f"/content/v1/cards/owners/{action}",
        body={"cardIds": card_ids, "cardOwners": card_owners},
    )


@mcp.tool()
def cards_remove_from_page(
    card_id: Annotated[str, "Card ID to remove"],
    page_id: Annotated[str, "Page ID to remove the card from"],
) -> Any:
    """Remove a card from a specific page."""
    return auth.post(f"/kpis/{card_id}/remove", pageid=page_id)


@mcp.tool()
def cards_remove_access(
    resource_id: Annotated[str, "Card ID to remove access from"],
    user_id: Annotated[str, "User ID to remove access for"],
) -> Any:
    """Remove a user's access from a card."""
    return auth.delete_root("/share/unsharekpiuser", resourceId=resource_id, userId=user_id)


@mcp.tool()
def cards_delete(
    card_ids: Annotated[str, "Comma-separated card IDs to delete"],
) -> Any:
    """Delete one or more cards."""
    return auth.delete("/content/v1/cards/bulk", cardIds=card_ids)


@mcp.tool()
def cards_delete_drill_path(
    card_id: Annotated[str, "Card ID"],
    drill_number: Annotated[str, "Drill level number"],
    drill_path_id: Annotated[str, "Drill path ID to delete"],
) -> Any:
    """Delete a drill path entry from a card."""
    return auth.delete(f"/kpis/{card_id}/drillPath/{drill_number}/drillView/{drill_path_id}")


# ---------------------------------------------------------------------------
# Problems (Issues)
# ---------------------------------------------------------------------------

@mcp.tool()
def cards_get_problems(
    urns: Annotated[str, "Comma-separated card URNs to retrieve problems for"],
    parts: Annotated[str | None, "Comma-separated parts to include (add 'problems' to get issues)"] = None,
) -> Any:
    """Get problem/issue records for one or more cards."""
    return auth.get("/content/v1/cards", urns=urns, parts=parts)


@mcp.tool()
def cards_create_problem(
    card_id: Annotated[str, "Card ID to attach the problem to"],
    message: Annotated[str, "Problem description text"],
) -> Any:
    """Create a problem (issue) on a card."""
    return auth.post(f"/content/v1/badges/{card_id}/problems", body=message)


@mcp.tool()
def cards_resolve_problem(
    card_id: Annotated[str, "Card ID"],
    problem_id: Annotated[str, "Problem ID to resolve"],
    state: Annotated[str | None, "Resolution state (e.g. 'RESOLVED')"] = None,
) -> Any:
    """Update the state of a card problem (e.g. mark it resolved)."""
    body: dict[str, Any] = {}
    if state is not None:
        body["state"] = state
    return auth.put(f"/content/v1/badges/{card_id}/problems/{problem_id}/states", body=body)
