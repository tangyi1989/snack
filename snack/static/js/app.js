// this a test js

window.App = Ember.Application.create();

App.ApplicationView = Ember.View.extend({
	templateName: 'application'
});
App.ApplicationController = Ember.Controller.extend({});

App.Router = Ember.Router.extend({
	root: Ember.Route.extend({
		index: Ember.Route.extend({
			route: '/',
			enter: function(router) {
				console.log('Entered root index.');
			},
			exit: function(router) {
				console.log('Exit root index.');
			},
		}),
	}),
});

App.initialize();

