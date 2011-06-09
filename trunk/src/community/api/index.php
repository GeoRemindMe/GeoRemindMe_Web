<?php
require '../h2o/h2o.php';
require '../templates/menu_sections.php';
h2o::load('i18n');

$var_template='api.html';
$var_title='APIs';
$active_section= 'APIs'; //Values= Names on ../templates/menu_sections.php

$template = new H2o('../templates/'.$var_template, array(
    'cache_dir' => dirname(__FILE__),
    'searchpath' => 'h2o',
    
    /*'i18n' => array(
		'locale' => 'fr',
	)*/
));

echo $template->render(array(
	'title'=> $var_title,
	'menu_items'=>$menu_sections,
	'active_section'=>$active_section,
	)
);


