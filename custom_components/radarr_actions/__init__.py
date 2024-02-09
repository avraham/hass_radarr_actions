"""The Radarr component."""
from __future__ import annotations

from typing import Any, Dict, cast



# from aiopyarr.models.host_configuration import PyArrHostConfiguration
# from aiopyarr.radarr_client import RadarrClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_SW_VERSION,
    CONF_API_KEY,
    CONF_URL,
    CONF_VERIFY_SSL,
    Platform,
)
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse, callback
from homeassistant.helpers.typing import ConfigType

import datetime
import requests
import json
import sys
import os
import configparser
import argparse
import logging

_LOGGER = logging.getLogger(__name__)
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
# from homeassistant.helpers.entity import EntityDescription
# from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_NAME, DOMAIN, ATTR_HOST, ATTR_API_KEY, ATTR_MOVIE_TITLE,
    ATTR_PROFILE_ID, ATTR_ROOT_DIRECTORY, ATTR_TMDBID_API_V3, BASE_URL, HEADERS,
    ATTR_LAST_N_YEARS, DEFAULT_LAST_N_YEARS, ATTR_SEARCH_RELEASE, DEFAULT_SEARCH_RELEASE,
    TMDBID_BASE_URL
)

from .hass_radarr_search_by_voice import MovieDownloader


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:

  
    """Set up the an async service example component."""
    @callback
    async def add_movie(call: ServiceCall) -> ServiceResponse:
        """My first service."""
        _LOGGER.info('Received data', call.data)

        response = Dict[str, Any]

        movie = call.data.get(ATTR_MOVIE_TITLE)
        host = call.data.get(ATTR_HOST)
        root_directory = call.data.get(ATTR_ROOT_DIRECTORY)
        profile_id = call.data.get(ATTR_PROFILE_ID)
        api_key = call.data.get(ATTR_API_KEY)
        tmdbid_api_key_v3 = call.data.get(ATTR_TMDBID_API_V3)


        range_of_years = call.data.get(ATTR_LAST_N_YEARS, DEFAULT_LAST_N_YEARS)
        search_release = call.data.get(ATTR_SEARCH_RELEASE, DEFAULT_SEARCH_RELEASE)


        obj = MovieDownloader(host, api_key, root_directory, profile_id, tmdbid_api_key_v3)
        r = await hass.async_add_executor_job(obj.search, movie, 0, range_of_years, search_release )
        if r["data"] != None and r["data"] != "":
            await hass.async_add_executor_job(hass.states.set, DOMAIN+".last_movie_id", int(r["data"]["id"]))
            
        return r
    
    # """Set up the an async service example component."""
    # @callback
    # async def add_upcoming_movie(call: ServiceCall) -> ServiceResponse:
    #     """My first service."""
    #     _LOGGER.info('Received data', call.data)

    #     response = Dict[str, Any]

    #     movie = call.data.get(ATTR_MOVIE_TITLE)
    #     host = call.data.get(ATTR_HOST)
    #     root_directory = call.data.get(ATTR_ROOT_DIRECTORY)
    #     profile_id = call.data.get(ATTR_PROFILE_ID)
    #     api_key = call.data.get(ATTR_API_KEY)
    #     tmdbid_api_key_v3 = call.data.get(ATTR_TMDBID_API_V3)


    #     range_of_years = 1

    #     obj = MovieDownloader(host, api_key, root_directory, profile_id, tmdbid_api_key_v3)
    #     r = await hass.async_add_executor_job(obj.search, movie, 0, range_of_years, False )
    #     if r["data"] != None and r["data"] != "":
    #         await hass.async_add_executor_job(hass.states.set, DOMAIN+".last_movie_id", int(r["data"]["id"]))
            
    #     return r
    
    """Set up the an async service example component."""
    @callback
    async def remove_movie(call: ServiceCall) -> ServiceResponse:
        """My first service."""
        _LOGGER.info('Received data', call.data)

        r = {
            "message" : "This was the failed request."

        }

        host = call.data.get(ATTR_HOST)
        api_key = call.data.get(ATTR_API_KEY)


        state = await hass.async_add_executor_job(hass.states.get, DOMAIN+".last_movie_id")

        if state != None:
            obj = MovieDownloader(host, api_key)
            r = await hass.async_add_executor_job(obj.remove_movie, state.state )
        
        return r
        

        # States are in the format DOMAIN.OBJECT_ID.
        # hass.states.set("radarr_actions.last_movie_added", 'Works!')

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, 'add_movie', add_movie, schema=None , supports_response=SupportsResponse.OPTIONAL)
    # hass.services.async_register(DOMAIN, 'add_upcoming_movie', add_upcoming_movie, schema=None , supports_response=SupportsResponse.OPTIONAL)
    hass.services.async_register(DOMAIN, 'remove_movie', remove_movie, schema=None , supports_response=SupportsResponse.OPTIONAL)


    # Return boolean to indicate that initialization was successfully.
    return True

