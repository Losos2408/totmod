module.exports = grammar({
    name: 'HoI4',
    extras: $ => [
        /\s|\r?\n/,
        $.comment,
    ],
    
    rules: {

        translation_unit: $ => choice(
            $.ideas_declarations,
			$.character_declarations,
            $.function_declarations,
            $.history_declaration,
            $.state_declaration,
        ),

		state_declaration: $ => seq(
            'state',
            '=',
            '{',
            repeat($._state_content),
            '}'
		),

		_state_content: $ => choice(
			$.id,
			$.name_declaration,
			$.state_manpower,
			$.state_category,
			$.resources_category,
			$.state_provinces,
			$.state_history,
			$.state_buildings_max,
			$.state_local_supplies,
			$.state_impassable,
		),

		state_category: $ => seq(
			'state_category',
			'=',
			$.identifier
		),

		resources_category: $ => seq(
			'resources',
			'=',
			'{',
			repeat($._identifier_number),
			'}'
		),

		state_manpower: $ => seq(
			'manpower',
			'=',
			$.number
		),

		state_buildings_max: $ => seq(
			'buildings_max_level_factor',
			'=',
			$.number
		),

		state_local_supplies: $ => seq(
			'local_supplies',
			'=',
			$.number
		),

		state_impassable: $ => seq(
			'impassable',
			'=',
			$.bool
		),

		state_provinces: $ => seq(
			'provinces',
			'=',
			'{',
			repeat1($.number),
			'}'
		),

		state_history: $ => seq(
			'history',
			'=',
			'{',
			repeat1($._state_history),
			'}'
		),

		_state_history: $ => choice(
			$.core_effect,
			$.victory_points,
			$.state_buildings,
			$.state_set_state_flag,
			$.state_set_demilitarized_zone,
			$.state_shared_buildings,
			$.state_set_resistance,
			$.state_set_compliance,
			$.state_force_disable_resistance,
		),

		core_effect: $ => seq(
			choice(
				'owner',
				'add_core_of',
				'add_claim_by'
			),
			'=',
			$.tag
		),

		victory_points: $ => seq(
			'victory_points',
			'=',
			'{',
			repeat1($.number),
			'}'
		),

		state_buildings: $ => seq(
			'buildings',
			'=',
			'{',
			repeat($._state_building),
			'}'
		),

		state_set_state_flag: $ => seq(
			'set_state_flag',
			'=',
			$.identifier
		),

		state_set_demilitarized_zone: $ => seq(
			'set_demilitarized_zone',
			'=',
			$.bool
		),

		state_shared_buildings: $ => seq(
			'add_extra_state_shared_building_slots',
			'=',
			$.number
		),

		state_set_resistance: $ => seq(
			'set_resistance',
			'=',
			$.number
		),

		state_set_compliance: $ => seq(
			'set_compliance',
			'=',
			$.number
		),

		state_force_disable_resistance: $ => seq(
			'force_disable_resistance',
			'=',
			$.bool
		),

		_state_building: $ => choice(
			$._identifier_number,
			$.province_buildings
		),

		province_buildings: $ => seq(
			$.number,
			'=',
			'{',
			repeat($._identifier_number),
			'}'
		),

        ideas_declarations: $ => seq(
            'ideas',
            '=',
            '{',
            repeat($._top_level_idea),
            '}'
        ),
        
        _top_level_idea: $ => choice(
            $.country_idea_block,
            $.law_idea_block
        ),

        country_idea_block: $ => seq(
            'country',
            '=',
            '{',
            repeat($.mid_level_idea),
            '}'
        ),

        character_declarations: $ => seq(
            'characters',
            '=',
            '{',
            repeat($.character),
            '}'
        ),

		character: $ => seq(
			$.identifier,
			'=',
			'{',
			repeat($._character_content),
			'}'
		),

		_character_content: $ => choice(
			$.name_declaration,
			$.character_portraits,
			$.character_country_leader,
			$.character_advisor,
			$.character_commander
		),

		character_portraits: $ => seq(
			'portraits',
			'=',
			'{',
			repeat($.character_portrait),
			'}'
		),

		character_portrait: $ => seq(
			choice(
				'civilian',
				'army',
				'navy'
			),
			'=',
			'{',
			repeat($._character_portrait_content),
			'}'
		),

		_character_portrait_content: $ => seq(
			choice(
				'large',
				'small'
			),
			'=',
			$._gfx
		),

		character_country_leader: $ => seq(
			'country_leader',
			'=',
			'{',
			repeat($._country_leader_content),
			'}'
		),

		_country_leader_content: $ => choice(
			$.desc,
			$.expire,
			$.ideology,
			$.id,
			$.traits,
		),

		character_advisor: $ => seq(
			'advisor',
			'=',
			'{',
			repeat($._advisor_content),
			'}'
		),

		_advisor_content: $ => choice(
			$.traits,
			$.idea_advisor_content,
			$._idea_content
		),

		idea_advisor_content: $ => seq(
			choice(
				'slot',
				'idea_token'
			),
			'=',
			$.identifier
		),

		character_commander: $ => seq(
			choice(
				'field_marshal',
				'corps_commander',
				'navy_leader'
			),
			'=',
			'{',
			repeat($._commander_content),
			'}'
		),

		_commander_content: $ => choice(
			$.traits,
			$.id,
			$.skill
		),

        function_declarations: $ => repeat1(
    		$.function_declaration
        ),

        function_declaration: $ => seq(
            $.identifier,
            '=',
            $.effect_block
        ),

        history_declaration: $ => repeat1(
        	$._history_effect
        ),

		_history_effect: $ => choice(
			$.capital_declaration,
			$._effect
		),

		capital_declaration: $ => seq(
			'capital',
			'=',
			$.state_id
		),

        law_idea_block: $ => seq(
            $.identifier,
            '=',
            '{',
            optional($.law_yes),
            repeat($.mid_level_idea),
            '}'
        ),

        law_yes: $ => seq(
            'law',
            '=',
            $.bool
        ),

        mid_level_idea: $ => seq(
            $.identifier,
            '=',
            $.idea_content
        ),

        idea_content: $ => seq(
            '{',
            repeat($._idea_content),
            '}'
        ),

        _idea_content: $ => choice(
            // Triggers
            $.idea_content_trigger,

            // Modifiers
            $.idea_modifiers,
            
            // Effects
            $.on_add,

            $.cost,
            $.ledger,
            $.picture,
            $.default,
            $.cancel_if_invalid
        ),

        idea_content_trigger: $ => seq(
            choice(
                'available',
                'allowed',
                'allowed_civil_war',
                'cancel',
                'ai_will_do'
            ),
            '=',
            $.trigger_block,
        ),

        idea_modifiers: $ => seq(
            'modifier',
            '=',
            $.modifier_block,
        ),

        on_add: $ => seq(
            'on_add',
            '=',
            $.effect_block,
        ),

        ledger: $ => seq(
            'ledger',
            '=',
            choice(
				'civilian',
				'hidden',
				'army',
				'air',
				'navy'
			)
        ),

        cost: $ => seq(
            choice(
				'cost',
				'removal_cost'
			),
            '=',
            $.number
        ),

        picture: $ => seq(
            'picture',
            '=',
            $.identifier
        ),

        default: $ => seq(
            'default',
            '=',
            $.bool
        ),

        cancel_if_invalid: $ => seq(
            'cancel_if_invalid',
            '=',
            $.bool
        ),

		// I put here everything related to the info about leaders
		desc: $ => seq(
			'desc',
			'=',
			$._loc_key_string
		),

		expire: $ => seq(
			'expire',
			'=',
			$.date
		),

		ideology: $ => seq(
			'ideology',
			'=',
			$.identifier
		),

		id: $ => seq(
			choice(
				'legacy_id',
				'id',
			),
			'=',
			$.number
		),

		skill: $ => seq(
			choice(
				'skill',
				'attack_skill',
				'defense_skill',
				'maneuvering_skill',
				'coordination_skill',
				'planning_skill',
				'logistics_skill'
			),
			'=',
			$.number
		),

		traits: $ => seq(
			'traits',
			'=',
			$.traits_block
		),


		// Block Stuff
        trigger_block: $ => seq(
            '{',
            repeat($._trigger),
            '}'
        ),

        modifier_block: $ => seq(
            '{',
            repeat($._modifier),
            '}'
        ),

        traits_block: $ => seq(
            '{',
            repeat($.identifier),
            '}'
        ),

        _trigger: $ => choice(
            $.check_variable,
            $.comp_trigger,
            $.trigger_scope_change,

			// Unique stuff
			$.has_dlc
        ),

		has_dlc: $ => seq(
			'has_dlc',
			'=',
			/".*"/
		),

        trigger_scope_change: $ => seq(
            $.identifier,
            "=",
            $.trigger_limit_block
        ),

        trigger_limit_block: $ => seq(
            '{',
            optional($.limit_trigger_block),
            repeat($._trigger),
            '}'
        ),

        check_variable: $ => seq(
            'check_variable',
            '=',
            '{',
            choice(
                $.check_variable_long,
                $.check_variable_short,
            ),
            '}'
        ),

        check_variable_long: $ => seq(
            'var',
            '=',
            choice(
                $.number,
                $.identifier
            ),
            'value',
            '=',
            choice(
                $.number,
                $.identifier
            ),
            'compare',
            '=',
            choice(
                'less_than',
                'less_than_or_equals',
                'greater_than',
                'greater_than_or_equals',
                'equals',
                'not_equals',
            ),
			optional(seq(
				'tooltip',
				'=',
				$._loc_key_string
			))
        ),

        check_variable_short: $ => seq(
            choice(
                $.number,
                $.identifier
            ),
            choice(
                "=",
                ">",
                "<"
            ),
            choice(
                $.number,
                $.identifier
            )
        ),

        comp_trigger: $ => seq(
            $.identifier,
            choice(
                "=",
                ">",
                "<"
            ),
            choice(
                $.number,
                $.identifier
            )
        ),

        _modifier: $ => choice(
            $.modifier,
            $.custom_modifier_tooltip
        ),

        modifier: $ => seq(
            $.identifier,
            "=",
            $.number
        ),

        custom_modifier_tooltip: $ => seq(
            'custom_modifier_tooltip',
            '=',
            $._loc_key_string
        ),

        _effect: $ => choice(
            // log is special
            $.log_effect, 

            // every effect = yes 
            $.scripted_effect,

            // any blahblah = { effects }
            $.scope_change,

            // Variable Math
            $.variable_math_effect,
            $.clamp_variable_effect,

			// Array Math
            $.array_math_effect,
            $.clear_array,

			// Generic Effects for hoi4 stuff
			$.identifier_effect,
			$.tag_effect,
			$.number_effect,
			$.character_effect,
			
            // stuff that is effect = { unique contents }
			$.ideas_effect,
			$.set_technology_effect,
			$.oob_effect,
            $.dynamic_modifier_effect,
            $.intelligence_agency_effect,
			$.set_autonomy_effect,
			$.set_politics_effect,
			$.set_popularities_effect,
			$.create_equipment_variant_effect,
			$.equipment_effect,
        ),

        log_effect: $ => seq(
            "log",
            "=",
            token(seq(
                "\"",
                /[^"]+/,
                "\""
            ))
        ),

        variable_math_effect: $ => seq(
            choice(
                // Normal
                'set_variable',
                'add_to_variable',
                'subtract_from_variable',
                'multiply_variable',
                'divide_variable',
                'modulo_variable',
                // Temp
                'set_temp_variable',
                'add_to_temp_variable',
                'subtract_from_temp_variable',
                'multiply_temp_variable',
                'divide_temp_variable',
                'modulo_temp_variable'
            ),
            "=",
            $.variable_math_block
        ),

        array_math_effect: $ => seq(
            choice(
                // Normal
                'add_to_array',
                'remove_from_array',
                'resize_array',
                'find_highest_in_array',
                'find_lowest_in_array',
                // Temp
                'add_to_temp_array',
                'remove_from_temp_array',
                'resize_temp_array',
            ),
            "=",
            $.array_math_block
        ),

        clamp_variable_effect: $ => seq(
            choice(
                "clamp_variable",
                "clamp_temp_variable"
            ),
            '=',
            $.clamp_variable_block
        ),

        clamp_variable_block: $ => seq(
            "{",
            'var',
            '=',
            $.identifier,
            optional(seq(
                'min',
                '=',
                choice(
                    $.identifier,
                    $.number
                )
            )),
            optional(seq(
                'max',
                '=',
                choice(
                    $.identifier,
                    $.number
                )
            )),
            "}"
        ),

        variable_math_block: $ => seq(
            "{",
            choice(
                $.variable_math_effect_long,
                $.math_effect_short
            ),
            "}"
        ),

        array_math_block: $ => seq(
            "{",
            choice(
                $.array_math_effect_long,
                $.math_effect_short
            ),
            "}"
        ),

		number_effect: $ => seq(
			$._number_effect,
			'=',
			$.number
		),

		_number_effect: $ => choice(
			'set_research_slots',
			'set_convoys',
			'set_war_support',
			'set_stability',
			'add_political_power'
		),

		identifier_effect: $ => seq(
			$._identifier_effect,
			'=',
			$.identifier
		),

		_identifier_effect: $ => choice(
			'set_country_flag',
			'create_faction',
			'complete_national_focus',
		),

		tag_effect: $ => seq(
			$._tag_effect,
			'=',
			$.tag
		),

		_tag_effect: $ => choice(
			'add_to_faction',
		),

		character_effect: $ => seq(
			'recruit_character',
			'=',
			$.identifier
		),

		ideas_effect: $ => seq(
			$._ideas_effect,
			'=',
			'{',
			repeat1($.identifier),
			'}'
		),

		_ideas_effect: $ => choice(
			'add_ideas',
			'remove_idea'
		),

		set_technology_effect: $ => seq(
			'set_technology',
			'=',
			'{',
			repeat($.technology_effect),
			'}'
		),

		technology_effect: $ => seq(
			$.identifier,
			'=',
			choice('1', '2')
		),

		oob_effect: $ => seq(
			$._oob_effect,
			'=',
			/".*"/
		),

		_oob_effect: $ => choice(
			choice(
				'set_naval_oob',
				'set_oob',
				'set_keyed_oob',
				'load_oob'
			),
		),

        dynamic_modifier_effect: $ => seq(
            choice(
                'add_dynamic_modifier',
                'remove_dynamic_modifier'
            ),
            '=',
            '{',
            'modifier',
            '=',
            $.identifier,
            optional(seq(
                'scope',
                '=',
                $.identifier
            )),
            optional(seq(
                'days',
                '=',
                $.number
            )),
            '}'
        ),

        intelligence_agency_effect: $ => seq(
            'create_intelligence_agency',
            '=',
            '{',
			repeat($._intelligence_agency_effect_content),
            '}'
        ),

        _intelligence_agency_effect_content: $ => choice(
            $.name_declaration,
			$.icon_declaration
        ),

        set_autonomy_effect: $ => seq(
            'set_autonomy',
            '=',
            '{',
			repeat($._set_autonomy_effect_content),
            '}'
        ),

        _set_autonomy_effect_content: $ => choice(
            $.target_declaration,
			$.set_autonomy_effect_level
        ),
		
		set_autonomy_effect_level: $ => seq(
			'autonomy_state',
			'=',
			$.identifier
		),

        set_politics_effect: $ => seq(
            'set_politics',
            '=',
            '{',
			repeat($._set_politics_effect_content),
            '}'
        ),

        _set_politics_effect_content: $ => choice(
            $.set_politics_effect_ruling_party,
            $.set_politics_effect_elections_allowed,
            $.set_politics_effect_last_election,
            $.set_politics_effect_election_frequency,
            $.set_politics_effect_long_name,
			$.name_declaration
        ),
		
		set_politics_effect_ruling_party: $ => seq(
			'ruling_party',
			'=',
			$.identifier
		),
		
		set_politics_effect_elections_allowed: $ => seq(
			'elections_allowed',
			'=',
			$.bool
		),
		
		set_politics_effect_last_election: $ => seq(
			'last_election',
			'=',
			$.date
		),
		
		set_politics_effect_election_frequency: $ => seq(
			'election_frequency',
			'=',
			$.number
		),
		
		set_politics_effect_long_name: $ => seq(
			'long_name',
			'=',
			$._loc_key_string
		),

		set_popularities_effect: $ => seq(
			'set_popularities',
			'=',
			'{',
			repeat($._set_popularities_effect_content),
			'}'
		),

		_set_popularities_effect_content: $ => seq(
			$.identifier,
			'=',
			$.number
		),

		create_equipment_variant_effect: $ => seq(
			'create_equipment_variant',
			'=',
			'{',
			repeat($._create_equipment_variant_effect_content),
			'}'
		),
		
		_create_equipment_variant_effect_content: $ => choice(
			$.name_declaration,
			$.icon_declaration,
			$.type_declaration,
			$.create_equipment_variant_effect_parent_version,
			$.create_equipment_variant_effect_obsolete,
			$.create_equipment_variant_effect_name_group,
			$.create_equipment_variant_effect_role_icon_index,
			$.create_equipment_variant_effect_model,
			$.create_equipment_variant_effect_upgrades,
			$.create_equipment_variant_effect_modules,
		),

		create_equipment_variant_effect_parent_version: $ => seq(
			'parent_version',
			'=',
			/[0-9]+/
		),

		create_equipment_variant_effect_obsolete: $ => seq(
			'obsolete',
			'=',
			$.bool
		),

		create_equipment_variant_effect_name_group: $ => seq(
			'name_group',
			'=',
			$.identifier
		),

		create_equipment_variant_effect_role_icon_index: $ => seq(
			'role_icon_index',
			'=',
			choice(
				'auto',
				/[0-9]+/
			)
		),

		create_equipment_variant_effect_model: $ => seq(
			'model',
			'=',
			$._loc_key_string
		),

		create_equipment_variant_effect_upgrades: $ => seq(
			'upgrades',
			'=',
			'{',
			repeat(seq(
				$.identifier,
				'=',
				/[0-9]+/
			)),
			'}'
		),

		create_equipment_variant_effect_modules: $ => seq(
			'modules',
			'=',
			'{',
			repeat(seq(
				$.identifier,
				'=',
				$.identifier
			)),
			'}'
		),

        equipment_effect: $ => seq(
            $._equipment_effect,
            '=',
            '{',
			repeat($._equipment_effect_content),
            '}'
        ),

		_equipment_effect: $ => choice(
			'set_equipment_fraction',
			'add_equipment_to_stockpile',
			'send_equipment',
			'send_equipment_fraction',
		),

		_equipment_effect_content: $ => choice(
			$.type_declaration,
			$.target_declaration,
			$.equipment_amount,
			$.equipment_producer,
			$.equipment_variant_name,
		),

		equipment_amount: $ => seq(
			'amount',
			'=',
			choice(
				/[0-9]+/,
				$.identifier
			)
		),

		equipment_producer: $ => seq(
			'producer',
			'=',
			$.identifier
		),

		equipment_variant_name: $ => seq(
			'variant_name',
			'=',
			$._loc_key_string
		),

        clear_array: $ => seq(
            choice(
                'clear_array',
                'clear_temp_array'
            ),
            '=',
            $.identifier
        ),

        math_effect_short: $ => seq(
            $.identifier,
            "=",
            choice(
                $.identifier,
                $.number
            ),
        ),

        variable_math_effect_long: $ => seq(
            "var",
            "=",
            $.identifier,
            "value",
            "=",
            choice(
                $.identifier,
                $.number
            ),
        ),

        array_math_effect_long: $ => seq(
            "array",
            "=",
            $.identifier,
            "value",
            "=",
            choice(
                $.identifier,
                $.number
            ),
            optional(seq(
                'index',
                '=',
                choice(
                    $.identifier,
                    $.number
                ),
            ))
        ),

        scripted_effect: $ => seq(
            $.identifier,
            "=",
            "yes"
        ),

        scope_change: $ => seq(
            $.scope_change_id,
            "=",
            $.effect_block
        ),

		scope_change_id: $ => choice(
			// Array Scopes
			'random_scope_in_array',
			'for_each_scope_loop',
			'for_each_loop',

			// Flow effects
			'for_loop_effect',
			'while_loop_effect',
			'if',
			
			// Actual Scopes
			'overlord',
			'faction_leader',
			'owner',
			'controller',
			'capital_scope',
			$.event_target,
			$.var_id,
			$.tag,
			$.state_id,

			// Pseudo scope
			'hidden_effect'
		),

        effect_block: $ => seq(
            '{',
            repeat($.for_loop_limits),
            optional($.limit_trigger_block),
            repeat($._effect),
            '}'
        ),

        for_loop_limits: $ => seq(
            choice(
                'start',
                'end',
                'value',
                'array',
                'break',
                'index',
            ),
            '=',
            choice(
                $.identifier,
                $.number
            )
        ),

        limit_trigger_block: $ => seq(
            'limit',
            '=',
            $.trigger_block,
        ),

		name_declaration: $ => seq(
			'name',
			'=',
			$._loc_key_string
		),

		icon_declaration: $ => seq(
			'icon',
			'=',
			$._gfx
		),
		
		type_declaration: $ => seq(
			'type',
			'=',
			$.identifier
		),
		
		target_declaration: $ => seq(
			'target',
			'=',
			$.tag
		),

		_identifier_number: $ => seq(
			$.identifier,
			'=',
			$.number
		),

        date: $ => /"[0-9]{1,4}.[0-9]{1,2}.[0-9]{1,2}"/,

        number: $ => token(seq(
            optional(/[-\+]/),
            choice(
                repeat1(/[0-9]/),
                seq(
                    repeat(/[0-9]/), 
                    '.',
                    repeat1(/[0-9]/), 
                )
            )
        )),

        identifier: $ => choice(
            /modifier@\w*/,
            /[a-zA-Z_]\w*\^?\w*/,
        ),

		event_target: $ => /event_target:\w+/,
		
		var_id: $ => /var_id:\w+\^?\w+/,

		state_id: $ => /[0-9]+/,

        tag: $ => choice(
			/[A-Z]{3}/,
			'ROOT',
			'THIS',
			'FROM',
			'PREV'
		),

		_gfx: $ => choice(
			$.gfx_string,
			$.gfx_key
		),

		gfx_string: $ => /".*"/,

        gfx_key: $ => /[a-zA-Z_]\w*/,

		_loc_key_string: $ => choice(
			$.loc_key,
			$.loc_key_enclosed,
			$.loc_string
		),

		loc_string: $ => /".*"/,

		loc_key_enclosed: $ => seq(
			'"',	
			$.loc_key,	
			'"'	
		),

        loc_key: $ => /[a-zA-Z_]\w*/,

		bool: $ => choice(
			'yes',
			'no'
		),

        comment: $ => token(
            seq('#', /(\\(.|\r?\n)|[^\\\n])*/),
        ),
    }
  });
  