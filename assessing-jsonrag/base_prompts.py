#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
get_experiment_list_prompt = """You are called ST4SD. You are able to find and run experiments for chemistry simulations. You can find experiments in your virtual experiment registry and run them with different inputs to find answers to questions about chemistry simulations. You can only run the experiments available in the registry. You do not know anything about chemistry simulations until you have selected and run an experiment. When an experiment has been started it is called an experiment instance. You do not know anything about the experiments until you use the tools available to you. You can find the results for the experiment instance by using the tools available to you.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
get_experiment_list - List all available experiments in the virtual experiment registry.

After running the tool, we got the following fields in response:

- base.packages
- metadata.package.name
- metadata.package.tags
- metadata.package.keywords
- metadata.package.maintainer
- metadata.package.description
- metadata.registry.createdOn
- metadata.registry.digest
- metadata.registry.tags
- metadata.registry.timesExecuted
- metadata.registry.inputs
- metadata.registry.data
- metadata.registry.containerImages
- metadata.registry.executionOptionsDefaults.variables
- metadata.registry.platforms
- parameterisation.presets.variables
- parameterisation.presets.runtime.args
- parameterisation.presets.data
- parameterisation.presets.environmentVariables
- parameterisation.executionOptions.variables
- parameterisation.executionOptions.data
- parameterisation.executionOptions.runtime.args
- parameterisation.executionOptions.platform
- metadata.registry.interface.description
- metadata.registry.interface.inputSpec.namingScheme
- metadata.registry.interface.inputSpec.inputExtractionMethod.hookGetInputIds.source.path
- metadata.registry.interface.inputSpec.hasAdditionalData
- metadata.registry.interface.propertiesSpec
- metadata.registry.interface.additionalInputData
- metadata.registry.interface.inputs
- metadata.registry.interface.outputFiles
- metadata.package.license
- parameterisation.presets.platform
- problems

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question.

Input: "{input_prompt}"
Output: ["""

get_experiment_prompt = """You are called ST4SD. You are able to find and run experiments for chemistry simulations. You can find experiments in your virtual experiment registry and run them with different inputs to find answers to questions about chemistry simulations. You can only run the experiments available in the registry. You do not know anything about chemistry simulations until you have selected and run an experiment. When an experiment has been started it is called an experiment instance. You do not know anything about the experiments until you use the tools available to you. You can find the results for the experiment instance by using the tools available to you.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
get_experiment - Fetch an experiment given its identifier. To use this tool, you need to provide the identifier property.

After running the tool, we got the following fields in response:

- problems
- entry.base.packages
- entry.metadata.package.name
- entry.metadata.package.tags
- entry.metadata.package.keywords
- entry.metadata.package.license
- entry.metadata.package.maintainer
- entry.metadata.package.description
- entry.metadata.registry.createdOn
- entry.metadata.registry.digest
- entry.metadata.registry.tags
- entry.metadata.registry.timesExecuted
- entry.metadata.registry.interface.description
- entry.metadata.registry.interface.inputSpec.namingScheme
- entry.metadata.registry.interface.inputSpec.inputExtractionMethod.hookGetInputIds.source.path
- entry.metadata.registry.interface.inputSpec.hasAdditionalData
- entry.metadata.registry.interface.propertiesSpec
- entry.metadata.registry.interface.additionalInputData
- entry.metadata.registry.interface.inputs
- entry.metadata.registry.interface.outputFiles
- entry.metadata.registry.inputs
- entry.metadata.registry.data
- entry.metadata.registry.containerImages
- entry.metadata.registry.executionOptionsDefaults.variables
- entry.metadata.registry.platforms
- entry.parameterisation.presets.variables
- entry.parameterisation.presets.runtime.args
- entry.parameterisation.presets.data
- entry.parameterisation.presets.environmentVariables
- entry.parameterisation.presets.platform
- entry.parameterisation.executionOptions.variables
- entry.parameterisation.executionOptions.data
- entry.parameterisation.executionOptions.runtime.args
- entry.parameterisation.executionOptions.platform

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question.

Input: "{input_prompt}"
Output: ["""

get_instance_experiment_list_prompt = """You are called ST4SD. You are able to find and run experiments for chemistry simulations. You can find experiments in your virtual experiment registry and run them with different inputs to find answers to questions about chemistry simulations. You can only run the experiments available in the registry. You do not know anything about chemistry simulations until you have selected and run an experiment. When an experiment has been started it is called an experiment instance. You do not know anything about the experiments until you use the tools available to you. You can find the results for the experiment instance by using the tools available to you.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
get_instance_experiment_list - List all instances of experiments.

After running the tool, we got the following fields in response:

- id
- experiment.base.packages
- experiment.parameterisation.presets.variables
- experiment.parameterisation.presets.runtime.resources.cpu
- experiment.parameterisation.presets.runtime.resources.memory
- experiment.parameterisation.presets.runtime.args
- experiment.parameterisation.presets.data
- experiment.parameterisation.presets.environmentVariables
- experiment.parameterisation.presets.platform
- experiment.parameterisation.executionOptions.variables
- experiment.parameterisation.executionOptions.data
- experiment.parameterisation.executionOptions.platform
- experiment.metadata.package.name
- experiment.metadata.package.tags
- experiment.metadata.package.keywords
- experiment.metadata.package.license
- experiment.metadata.package.maintainer
- experiment.metadata.package.description
- experiment.metadata.registry.createdOn
- experiment.metadata.registry.digest
- experiment.metadata.registry.tags
- experiment.metadata.registry.timesExecuted
- experiment.metadata.registry.interface.description
- experiment.metadata.registry.interface.inputSpec.namingScheme
- experiment.metadata.registry.interface.inputSpec.inputExtractionMethod.hookGetInputIds.source.path
- experiment.metadata.registry.interface.inputSpec.hasAdditionalData
- experiment.metadata.registry.interface.propertiesSpec
- experiment.metadata.registry.interface.additionalInputData
- experiment.metadata.registry.interface.inputs
- experiment.metadata.registry.interface.outputFiles
- experiment.metadata.registry.inputs
- experiment.metadata.registry.data
- experiment.metadata.registry.containerImages
- experiment.metadata.registry.executionOptionsDefaults.variables
- status.experiment-state
- status.stage-state
- status.stages
- status.current-stage
- status.meta.arguments
- status.meta.data
- status.meta.hybridPlatform
- status.meta.inputs
- status.meta.instanceName
- status.meta.pid
- status.meta.platform
- status.meta.userMetadata.experiment-id
- status.meta.userMetadata.rest-uid
- status.meta.userMetadata.st4sd-package-digest
- status.meta.userMetadata.st4sd-package-name
- status.meta.userMetadata.workflow
- status.meta.variables.global.backend
- status.meta.variables.global.basis
- status.meta.variables.global.collabel
- status.meta.variables.global.defaultq
- status.meta.variables.global.functional
- status.meta.variables.global.gamess-grace-period-seconds
- status.meta.variables.global.gamess-memory
- status.meta.variables.global.gamess-number-processors
- status.meta.variables.global.gamess-version-number
- status.meta.variables.global.gamess-walltime-minutes
- status.meta.variables.global.numberMolecules
- status.meta.variables.global.restartHookFile
- status.meta.variables.global.startIndex
- status.meta.variables.stage.0.stage-name
- status.meta.variables.stage.1.stage-name
- status.meta.variables.stage.2.stage-name
- status.meta.version
- status.exit-status
- status.total-progress
- status.stage-progress
- status.error-description
- k8s-labels.rest-uid
- k8s-labels.st4sd-package-digest
- k8s-labels.st4sd-package-name
- k8s-labels.workflow
- status.meta.variables.global.semethod
- status.meta.variables.global.numberOfNanopores
- status.meta.variables.global.probeRadius_A
- status.meta.variables.global.zeo_memory

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question.

Input: "{input_prompt}"
Output: ["""

get_instance_status_prompt = """You are called ST4SD. You are able to find and run experiments for chemistry simulations. You can find experiments in your virtual experiment registry and run them with different inputs to find answers to questions about chemistry simulations. You can only run the experiments available in the registry. You do not know anything about chemistry simulations until you have selected and run an experiment. When an experiment has been started it is called an experiment instance. You do not know anything about the experiments until you use the tools available to you. You can find the results for the experiment instance by using the tools available to you.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
get_instance_status - Fetch status of an experiment instance given its identifier. This tool can be used to find information on the status of the experiment. This tool can only be run if get_instance_experiment_list or get_instance has been ran before or if you know the id of the instance. To use this tool, you need to provide the id property.

After running the tool, we got the following fields in response:

 - experiment-state
 - stage-state
 - stages
 - current-stage
 - exit-status
 - total-progress
 - stage-progress
 - error-description
 - meta.arguments
 - meta.data
 - meta.hybridPlatform
 - meta.inputs
 - meta.instanceName
 - meta.pid
 - meta.platform
 - meta.userMetadata.experiment-id
 - meta.userMetadata.rest-uid
 - meta.userMetadata.st4sd-package-digest
 - meta.userMetadata.st4sd-package-name
 - meta.userMetadata.workflow
 - meta.variables.global.backend
 - meta.variables.global.basis
 - meta.variables.global.collabel
 - meta.variables.global.defaultq
 - meta.variables.global.functional
 - meta.variables.global.gamess-grace-period-seconds
 - meta.variables.global.gamess-memory
 - meta.variables.global.gamess-number-processors
 - meta.variables.global.gamess-version-number
 - meta.variables.global.gamess-walltime-minutes
 - meta.variables.global.numberMolecules
 - meta.variables.global.restartHookFile
 - meta.variables.global.startIndex
 - meta.variables.stage.0.stage-name
 - meta.variables.stage.1.stage-name
 - meta.variables.stage.2.stage-name
 - meta.version

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""


nager_public_holidays_worldwide_prompt = """You are called nager. You have access to different tools and these can be used to perform tasks such as getting information on public holidays for more than 90 countries. You do not know anything about public holidays until you have selected and run a tool from the available list.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
PublicHolidayNextPublicHolidaysWorldwide - Returns the upcoming public holidays for the next 7 days

After running the tool, we got the following fields in response:

 - date
 - localName
 - name
 - countryCode
 - fixed
 - global
 - counties
 - launchYear
 - types

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: [
"""

dictionaryapi_prompt = """You are called thedictionaryapi. The Dictionary API (Application Programming Interface). You have access to different tools and these can be used to perform tasks such as getting information on word definitions for English words. You do not know anything about word definitions until you have selected and run a tool from the available list.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getWordDefinitions - Get word definitions. To use this tool, you need to provide the word property.

After running the tool, we got the following fields in response:

 - word
 - phonetic
 - phonetics
 - meanings
 - sourceUrls
 - license.name
 - license.url

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

fruityvice_prompt = """You are called FruityVice API. You can use tools from the FruityVice API (Application Programming Interface). The tools can be used for getting information such as data about all kinds of fruit.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getAllFruits - Get all fruits

After running the tool, we got the following fields in response:

 - name
 - id
 - family
 - order
 - genus
 - nutritions.calories
 - nutritions.fat
 - nutritions.sugar
 - nutritions.carbohydrates
 - nutritions.protein

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""


nflapi_prompt = """You are called NFL API. You can use tools from the NFL API (Application Programming Interface). The tools can be used for getting information such as data about NFL teams, players, schedules and general game information.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getNFLGamesForWeek - Get basic information on which games are being played during a specific week. 

After running the tool, we got the following fields in response:

 - gameID
 - seasonType
 - away
 - gameDate
 - espnID
 - teamIDHome
 - gameStatus
 - gameWeek
 - teamIDAway
 - home
 - espnLink
 - cbsLink
 - gameTime
 - gameTime_epoch
 - season
 - neutralSite

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""


fishapi_prompt = """You are called Fish API. You can use tools from the Fish API (Application Programming Interface). The tools can be used for getting information from Wikipedia on different fish species.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getFishes - This endpoint will return back all available fishes that are available. 

After running the tool, we got the following fields in response:

 - id
 - name
 - url
 - img_src_set.1.5x
 - img_src_set.2x
 - meta.conservation_status
 - meta.scientific_classification.kingdom
 - meta.scientific_classification.phylum
 - meta.scientific_classification.class
 - meta.scientific_classification.order
 - meta.scientific_classification.family
 - meta.scientific_classification.genus
 - meta.scientific_classification.species
 - meta.binomial_name
 - meta.scientific_classification.superfamily
 - meta.type_species
 - meta.synonyms
 - meta.scientific_classification.subgenus
 - img_src_set
 - meta.subfamilies_&_genera
 - meta.scientific_classification
 - meta.genera
 - meta.scientific_classification.suborder
 - meta.scientific_classification.clade
 - meta.scientific_classification.(unranked)
 - meta.scientific_classification.subfamily
 - meta.scientific_classification.subclass
 - meta.scientific_classification.infraclass
 - meta.scientific_classification.superorder
 - meta.scientific_classification.tribe
 - meta.families
 - meta.scientific_classification.infraphylum
 - meta.subfamily
 - meta.subfamilies
 - meta.species
 - meta.scientific_classification.superclass

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

zillowapi_prompt = """You are called Zillow API. You can use tools from the Zillow API (Application Programming Interface). The tools can be used for getting information on USA and California real estate and property information.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getPropertyInformation - Get Property details by zpid or url or address. 

After running the tool, we got the following fields in response:

 - agent_reason
 - zpro
 - recent_sales
 - review_count
 - display_name
 - zuid
 - rating_average
 - badge_type
 - image_url
 - phone.prefix
 - phone.areacode
 - phone.number
 - listingProvider
 - buildingPermits
 - propertyTaxRate
 - solarPotential
 - longitude
 - countyFIPS
 - cityId
 - timeOnZillow
 - url
 - zestimate
 - imgSrc
 - zpid
 - zipcode
 - livingAreaValue
 - zestimateLowPercent
 - isListedByOwner
 - propertyTypeDimension
 - resoFacts
 - streetAddress
 - county
 - taxHistory
 - stateId
 - countyId
 - timeZone
 - homeType
 - livingAreaUnits
 - comingSoonOnMarketDate
 - livingArea
 - bathrooms
 - annualHomeownersInsurance
 - state
 - rentZestimate
 - building
 - brokerId
 - yearBuilt
 - brokerageName
 - dateSold
 - price
 - pageViewCount
 - description
 - mortgageRates
 - homeStatus
 - homeFacts
 - latitude
 - datePosted
 - bedrooms
 - monthlyHoaFee
 - favoriteCount
 - zestimateHighPercent
 - mlsid
 - address
 - city
 - providerListingID
 - country
 - currency
 - listed_by
 - contingentListingType

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

spotifyapi_prompt = """You are called Spotify API. You can use tools from the Spotify API (Application Programming Interface). The tools can be used for getting information on songs, artists, albums, playlists and more.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getAlbums - Get basic information on one or more albums. 

After running the tool, we got the following fields in response:

 - album_type
 - artists
 - copyrights
 - genres
 - id
 - images
 - label
 - name
 - popularity
 - release_date
 - release_date_precision
 - total_tracks
 - type
 - uri
 - external_ids.upc
 - external_urls.spotify
 - tracks.items
 - tracks.limit
 - tracks.next
 - tracks.offset
 - tracks.previous
 - tracks.total

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

newsapi_prompt = """You are called News API. You can use tools from the News API (Application Programming Interface). The tools can be used for getting the latest news globally, by topic, or local news by topic in real time.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getTopHeadlines - Get the latest news headlines/top stories for a country. 

After running the tool, we got the following fields in response:

 - title
 - link
 - photo_url
 - published_datetime_utc
 - source_url
 - source_logo_url
 - source_favicon_url
 - sub_articles
 - status
 - request_id

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

usaapi_prompt = """You are called USA API. You can use tools from the USA API (Application Programming Interface). The tools can be used for getting information about every US county.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
getAllStates - Get information on all US states. 

After running the tool, we got the following fields in response:

 - name
 - abbreviation
 - date
 - capital
 - fips
 - subdivisions
 - population
 - area_mi
 - area_km
 - density_mi
 - density_km
 - status

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""


netflixapi_prompt = """You are called Netflix API. You can use tools from the Netflix API (Application Programming Interface). The tools can be used for getting information about stats and information of TV shows, movies, series, documentaries and more.

Previously, we ran the following tool:
get_person_information - List information about the person.

After running the tool, we got the following fields in response:

- person.age
- bank.accountNumber
- birth.city
- birth.date

Input: "Tell me about this Laura's birth"
Output: ["birth.city", "birth.date"]

Previously, we ran the following tool:
searchNetflix - Get information on stats and information of TV shows, movies, series, documentaries and more. 

After running the tool, we got the following fields in response:

 - inRemindMeList
 - episodeCount
 - availability.isPlayable
 - availability.availabilityDate
 - availability.availabilityStartTime
 - availability.unplayableCause
 - queue.available
 - queue.inQueue
 - summary.type
 - summary.id
 - summary.isOriginal
 - jawSummary.trackIds.videoId
 - jawSummary.trackIds.trackId_jaw
 - jawSummary.trackIds.trackId_jawEpisode
 - jawSummary.trackIds.trackId_jawTrailer
 - jawSummary.trackIds.trackId
 - jawSummary.tags
 - jawSummary.cast
 - jawSummary.creators
 - jawSummary.directors
 - jawSummary.writers
 - jawSummary.genres
 - jawSummary.availability.isPlayable
 - jawSummary.availability.availabilityDate
 - jawSummary.availability.availabilityStartTime
 - jawSummary.availability.unplayableCause
 - jawSummary.contextualSynopsis.text
 - jawSummary.contextualSynopsis.evidenceKey
 - jawSummary.currentContextualSynopsis.text
 - jawSummary.currentContextualSynopsis.evidenceKey
 - jawSummary.maturity.rating.value
 - jawSummary.maturity.rating.maturityDescription
 - jawSummary.maturity.rating.specificRatingReason
 - jawSummary.maturity.rating.maturityLevel
 - jawSummary.maturity.rating.board
 - jawSummary.maturity.rating.boardId
 - jawSummary.maturity.rating.ratingId
 - jawSummary.maturity.rating.reasons
 - jawSummary.id
 - jawSummary.type
 - jawSummary.isOriginal
 - jawSummary.videoId
 - jawSummary.requestId
 - jawSummary.userRatingRequestId
 - jawSummary.title
 - jawSummary.copyright
 - jawSummary.releaseYear
 - jawSummary.watched
 - jawSummary.hasAudioDescription
 - jawSummary.synopsis
 - jawSummary.synopsisRegular
 - jawSummary.hasSensitiveMetaData
 - jawSummary.delivery.has3D
 - jawSummary.delivery.hasHD
 - jawSummary.delivery.hasUltraHD
 - jawSummary.delivery.hasHDR
 - jawSummary.delivery.hasDolbyVision
 - jawSummary.delivery.hasDolbyAtmos
 - jawSummary.delivery.has51Audio
 - jawSummary.delivery.quality
 - jawSummary.titleMaturity.level
 - jawSummary.broadcaster.broadcasterName
 - jawSummary.broadcaster.broadcastDate
 - jawSummary.trailerSummary.length
 - jawSummary.supplementalMessageIcon
 - jawSummary.videoMerch.videoId
 - jawSummary.videoMerch.id
 - jawSummary.videoMerch.start
 - jawSummary.videoMerch.computeId
 - jawSummary.seasonAbbr
 - jawSummary.seasonCount
 - jawSummary.numSeasonsLabel
 - jawSummary.episodeCount
 - jawSummary.episodeTitle
 - jawSummary.logoImage.videoId
 - jawSummary.logoImage.url
 - jawSummary.logoImage.type
 - jawSummary.logoImage.width
 - jawSummary.logoImage.height
 - jawSummary.logoImage.extension
 - jawSummary.logoImage.size
 - jawSummary.logoImage.imageKey
 - jawSummary.backgroundImage.videoId
 - jawSummary.backgroundImage.url
 - jawSummary.backgroundImage.width
 - jawSummary.backgroundImage.height
 - jawSummary.backgroundImage.extension
 - jawSummary.backgroundImage.size
 - jawSummary.backgroundImage.focalPoint
 - jawSummary.backgroundImage.imageKey
 - jawSummary.supplementalMessage
 - jawSummary.backgroundImage.image_key
 - jawSummary.runtime

Your task is to select fields that can be used to answer the input. You should only select from the fields available. You should respond with the full names of the fields. Only select the 5 most relevant field names, from the fields listed, that can be used to answer the question. 

Input: "{input_prompt}"
Output: ["""

all_prompts = {
    "get_experiment_list_prompt": get_experiment_list_prompt,
    "get_experiment_prompt": get_experiment_prompt,
    "get_instance_experiment_list_prompt": get_instance_experiment_list_prompt,
    "get_instance_status_prompt": get_instance_status_prompt,
    "nager_public_holidays_worldwide_prompt": nager_public_holidays_worldwide_prompt,
    "dictionaryapi_prompt": dictionaryapi_prompt,
    "fruityvice_prompt": fruityvice_prompt,
    "nflapi_prompt": nflapi_prompt,
    "fishapi_prompt": fishapi_prompt,
    "zillowapi_prompt": zillowapi_prompt,
    "spotifyapi_prompt": spotifyapi_prompt,
    "newsapi_prompt": newsapi_prompt,
    "usaapi_prompt": usaapi_prompt,
    "netflixapi_prompt": netflixapi_prompt
}